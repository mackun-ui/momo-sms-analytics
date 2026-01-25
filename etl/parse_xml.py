"""
XML Parsing module for MoMo SMS data
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any
import json
import re
from datetime import datetime


def parse_xml_file(xml_path: Path) -> List[Dict[str, Any]]:
    """
    Parse XML file and extract transaction records
    
    Args:
        xml_path: Path to the XML file
        
    Returns:
        List of dictionaries containing transaction data
    """
    transactions = []
    
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Extract SMS messages
    for idx, sms in enumerate(root.findall('sms'), start=1):
        body = sms.get('body', '')
        date_timestamp = sms.get('date', '')
        readable_date = sms.get('readable_date', '')
        
        # Parse transaction details from body text
        transaction = parse_transaction_body(body, idx, date_timestamp, readable_date)
        
        if transaction:
            transactions.append(transaction)
    
    return transactions


def parse_transaction_body(body: str, transaction_id: int, timestamp: str, readable_date: str) -> Dict[str, Any]:
    """
    Extract transaction details from SMS body text
    
    Args:
        body: SMS message body
        transaction_id: Unique ID for the transaction
        timestamp: Unix timestamp from SMS
        readable_date: Human-readable date
        
    Returns:
        Dictionary with transaction details
    """
    transaction = {
        "id": str(transaction_id),
        "body": body,
        "timestamp": timestamp,
        "readable_date": readable_date,
        "type": "UNKNOWN",
        "amount": 0.0,
        "fee": 0.0,
        "balance": 0.0,
        "sender": "",
        "receiver": "",
        "transaction_id_external": ""
    }
    
    # Pattern matching for different transaction types
    
    # Type 1: Received money
    received_pattern = r"You have received (\d+(?:,\d+)*) RWF from ([^(]+)\s*\([^)]+\).*Your new balance:(\d+(?:,\d+)*) RWF.*Transaction Id: (\d+)"
    received_match = re.search(received_pattern, body)
    if received_match:
        transaction["type"] = "RECEIVED"
        transaction["amount"] = float(received_match.group(1).replace(',', ''))
        transaction["sender"] = received_match.group(2).strip()
        transaction["receiver"] = "You"
        transaction["balance"] = float(received_match.group(3).replace(',', ''))
        transaction["transaction_id_external"] = received_match.group(4)
        return transaction
    
    # Type 2: Sent/Transferred money
    transfer_pattern = r"(\d+(?:,\d+)*) RWF transferred to ([^(]+)\s*\((\d+)\).*Fee was: (\d+(?:,\d+)*) RWF.*New balance: (\d+(?:,\d+)*) RWF"
    transfer_match = re.search(transfer_pattern, body)
    if transfer_match:
        transaction["type"] = "SENT"
        transaction["amount"] = float(transfer_match.group(1).replace(',', ''))
        transaction["receiver"] = transfer_match.group(2).strip()
        transaction["fee"] = float(transfer_match.group(4).replace(',', ''))
        transaction["balance"] = float(transfer_match.group(5).replace(',', ''))
        transaction["sender"] = "You"
        # Extract TxId if present
        txid_match = re.search(r'TxId:\s*(\d+)', body)
        if txid_match:
            transaction["transaction_id_external"] = txid_match.group(1)
        return transaction
    
    # Type 3: Payment to merchant/agent
    payment_pattern = r"TxId:\s*(\d+).*Your payment of (\d+(?:,\d+)*) RWF to ([^0-9]+)\s*\d+.*Your new balance:\s*(\d+(?:,\d+)*) RWF.*Fee was (\d+) RWF"
    payment_match = re.search(payment_pattern, body)
    if payment_match:
        transaction["type"] = "PAYMENT"
        transaction["transaction_id_external"] = payment_match.group(1)
        transaction["amount"] = float(payment_match.group(2).replace(',', ''))
        transaction["receiver"] = payment_match.group(3).strip()
        transaction["sender"] = "You"
        transaction["balance"] = float(payment_match.group(4).replace(',', ''))
        transaction["fee"] = float(payment_match.group(5).replace(',', ''))
        return transaction
    
    # Type 4: Bank deposit
    deposit_pattern = r"A bank deposit of (\d+(?:,\d+)*) RWF.*Your NEW BALANCE\s*:(\d+(?:,\d+)*) RWF"
    deposit_match = re.search(deposit_pattern, body)
    if deposit_match:
        transaction["type"] = "BANK_DEPOSIT"
        transaction["amount"] = float(deposit_match.group(1).replace(',', ''))
        transaction["balance"] = float(deposit_match.group(2).replace(',', ''))
        transaction["sender"] = "Bank"
        transaction["receiver"] = "You"
        return transaction
    
    # Type 5: Direct payment debit
    direct_payment_pattern = r"A transaction of (\d+(?:,\d+)*) RWF by ([^o]+) on.*Your new balance:(\d+(?:,\d+)*) RWF.*Fee was (\d+) RWF.*Transaction Id: (\d+)"
    direct_payment_match = re.search(direct_payment_pattern, body)
    if direct_payment_match:
        transaction["type"] = "DIRECT_PAYMENT"
        transaction["amount"] = float(direct_payment_match.group(1).replace(',', ''))
        transaction["receiver"] = direct_payment_match.group(2).strip()
        transaction["sender"] = "You"
        transaction["balance"] = float(direct_payment_match.group(3).replace(',', ''))
        transaction["fee"] = float(direct_payment_match.group(4).replace(',', ''))
        transaction["transaction_id_external"] = direct_payment_match.group(5)
        return transaction
    
    # Return unparsed transaction for logging
    return transaction


def save_to_json(transactions: List[Dict[str, Any]], output_path: Path) -> None:
    """
    Save transactions to JSON file
    
    Args:
        transactions: List of transaction dictionaries
        output_path: Path to output JSON file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(transactions)} transactions to {output_path}")


if __name__ == "__main__":
    # For testing
    xml_file = Path(__file__).parent.parent / "data" / "raw" / "modified_sms_v2.xml"
    output_file = Path(__file__).parent.parent / "data" / "processed" / "transactions.json"
    
    if xml_file.exists():
        transactions = parse_xml_file(xml_file)
        save_to_json(transactions, output_file)
        
        # Print summary
        print(f"\n📊 Parsing Summary:")
        print(f"   Total transactions: {len(transactions)}")
        
        # Count by type
        types = {}
        for t in transactions:
            types[t['type']] = types.get(t['type'], 0) + 1
        
        print(f"\n   Breakdown by type:")
        for t_type, count in types.items():
            print(f"   - {t_type}: {count}")
    else:
        print(f"❌ XML file not found at {xml_file}")
