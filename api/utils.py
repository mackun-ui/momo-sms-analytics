import re
from datetime import datetime


def generate_transaction_id(existing_ids=None):
    """Generate a new unique transaction ID"""
    if not existing_ids:
        return 1
    return max(existing_ids) + 1


def validate_transaction_data(transaction_data, required_fields=None, is_update=False):
    """
    Validate transaction data before saving.
    Returns (is_valid, error_message)
    """
    if required_fields is None:
        required_fields = ['type', 'amount', 'sender']
    
    if not isinstance(transaction_data, dict):
        return False, "Transaction data must be a dictionary"
    
    # For updates we don't need all fields
    if not is_update:
        missing_fields = [field for field in required_fields 
                         if field not in transaction_data]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    errors = []
    
    # Check amount is valid
    if 'amount' in transaction_data:
        try:
            amt = float(transaction_data['amount'])
            if amt < 0:
                errors.append("Amount must be positive")
        except (ValueError, TypeError):
            errors.append("Amount must be a valid number")
    
    # Validate transaction type
    if 'type' in transaction_data:
        valid_types = ['send', 'receive', 'deposit', 'withdraw', 'payment', 'transfer']
        trans_type = str(transaction_data['type']).lower()
        if trans_type not in valid_types:
            errors.append(f"Type must be one of: {', '.join(valid_types)}")
    
    # Sender can't be empty
    if 'sender' in transaction_data:
        if not transaction_data['sender'] or str(transaction_data['sender']).strip() == '':
            errors.append("Sender cannot be empty")
    
    # Receiver validation (if provided)
    if 'receiver' in transaction_data:
        receiver = transaction_data['receiver']
        if receiver and str(receiver).strip() == '':
            errors.append("Receiver cannot be empty if provided")
    
    # Check timestamp format
    if 'timestamp' in transaction_data:
        if not validate_timestamp(transaction_data['timestamp']):
            errors.append("Invalid timestamp format")
    
    # Phone number validation
    if 'sender_phone' in transaction_data:
        if not validate_phone_number(transaction_data['sender_phone']):
            errors.append("Invalid sender phone number format")
    
    if 'receiver_phone' in transaction_data:
        if not validate_phone_number(transaction_data['receiver_phone']):
            errors.append("Invalid receiver phone number format")
    
    if errors:
        return False, "; ".join(errors)
    
    return True, None


def validate_timestamp(timestamp):
    """Check if timestamp is in a valid format"""
    if not timestamp:
        return False
    
    # Try different date formats that we might receive
    date_formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d',
        '%d/%m/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S'
    ]
    
    for fmt in date_formats:
        try:
            datetime.strptime(str(timestamp), fmt)
            return True
        except ValueError:
            continue
    
    return False


def validate_phone_number(phone):
    """Basic phone number validation - checks if it's numeric and reasonable length"""
    if not phone:
        return False
    
    # Strip out common formatting characters
    phone_clean = str(phone).replace(' ', '').replace('-', '').replace('+', '')
    
    # Should be all digits and between 7-15 characters
    if phone_clean.isdigit() and 7 <= len(phone_clean) <= 15:
        return True
    
    return False


def sanitize_transaction_data(transaction_data):
    """Clean up transaction data by removing None values and trimming strings"""
    cleaned = {}
    
    for key, value in transaction_data.items():
        if value is None:
            continue
        
        if isinstance(value, str):
            cleaned[key] = value.strip()
        else:
            cleaned[key] = value
    
    return cleaned


def format_transaction_response(transaction):
    """Format transaction for API response - mostly just ensuring consistent types"""
    result = transaction.copy()
    
    # Format amount to 2 decimal places
    if 'amount' in result:
        try:
            result['amount'] = f"{float(result['amount']):.2f}"
        except (ValueError, TypeError):
            pass  # just leave it as-is if we can't convert
    
    # Make sure ID is integer
    if 'id' in result:
        try:
            result['id'] = int(result['id'])
        except (ValueError, TypeError):
            pass
    
    return result


def parse_transaction_id(id_string):
    """Parse transaction ID from string, returns None if invalid"""
    try:
        tid = int(id_string)
        if tid > 0:
            return tid
    except (ValueError, TypeError):
        pass
    
    return None


def create_error_response(message, status_code=400):
    """Helper to create standard error response"""
    return {
        'error': True,
        'message': message,
        'status_code': status_code
    }


def create_success_response(data, message=None):
    """Helper to create standard success response"""
    response = {
        'error': False,
        'data': data
    }
    
    if message:
        response['message'] = message
    
    return response


def extract_id_from_path(path):
    """
    Extract transaction ID from URL path like /transactions/123
    """
    pattern = r'/transactions/(\d+)'
    match = re.search(pattern, path)
    
    if match:
        return int(match.group(1))
    
    return None


def filter_transactions(transactions, filters):
    """Filter list of transactions by given criteria"""
    result = transactions
    
    for key, value in filters.items():
        if value is not None:
            result = [t for t in result if t.get(key) == value]
    
    return result


def get_transaction_summary(transactions):
    """Calculate summary stats for a list of transactions"""
    if not transactions:
        return {
            'total_count': 0,
            'total_amount': 0,
            'average_amount': 0
        }
    
    total = 0
    count = len(transactions)
    
    for trans in transactions:
        try:
            amount = float(trans.get('amount', 0))
            total += amount
        except (ValueError, TypeError):
            # skip invalid amounts
            pass
    
    avg = round(total / count, 2) if count > 0 else 0
    
    return {
        'total_count': count,
        'total_amount': round(total, 2),
        'average_amount': avg
    }
