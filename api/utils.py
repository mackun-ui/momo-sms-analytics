
import re
from datetime import datetime

def validate_transaction(transaction):
    required = ['type', 'amount', 'sender']
    
    for field in required:
        if field not in transaction:
            return False, f"Missing {field}"
    
    valid_types = ['send', 'receive', 'deposit', 'withdrawal', 'payment']
    if transaction['type'].lower() not in valid_types:
        return False, f"Type must be: {', '.join(valid_types)}"
    
    try:
        amount = float(transaction['amount'])
        if amount <= 0:
            return False, "Amount must be positive"
    except:
        return False, "Amount must be a number"
    
    sender = str(transaction['sender'])
    if not sender or len(sender) < 3:
        return False, "Invalid sender"
    
    return True, ""


def validate_amount(amount):
    try:
        num = float(amount)
        return num > 0
    except:
        return False


def validate_phone_number(phone):
    if not phone:
        return False
    
    cleaned = re.sub(r'[\s\-\(\)]', '', str(phone))
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15


def generate_transaction_id(existing_ids):
    if not existing_ids:
        return "1"
    
    numbers = []
    for id in existing_ids:
        try:
            numbers.append(int(id))
        except:
            pass
    
    if numbers:
        return str(max(numbers) + 1)
    else:
        return str(len(existing_ids) + 1)


def format_transaction_response(transaction):
    return {
        'id': transaction.get('id'),
        'type': transaction.get('type'),
        'amount': transaction.get('amount'),
        'sender': transaction.get('sender'),
        'receiver': transaction.get('receiver', 'N/A'),
        'timestamp': transaction.get('timestamp', datetime.now().isoformat()),
        'status': transaction.get('status', 'completed')
    }


def sanitize_input(data):
    if not isinstance(data, str):
        return data
    return data.strip()
