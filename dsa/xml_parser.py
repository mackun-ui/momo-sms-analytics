"""
XML Parser for MoMo SMS Transactions
Converts XML data to JSON format

Author: Role A - Data Parsing & DSA Lead
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any
import json
import re


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
    
    print(f"📄 Parsing XML file: {xml_path.name}")
    print(f"   Total SMS count: {root.get('count', 'unknown')}")
    
    # Extract SMS messages
    for idx, sms in enumerate(root.findall('sms'), start=1):
        body = sms.get('body', '')
        date_timestamp = sms.get('date', '')
        readable_date = sms.get('readable_date', '')
        
        # Parse transaction details from body text
        transaction = parse_transaction_body(body, idx, date_timestamp, readable_date)
        
        if transaction:
            transactions.append(transaction)
    
    print(f"✅ Successfully parsed {len(transactions)} transactions\n")
    return transactions


def parse_transaction_body(body: str, transaction_id: int, timestamp: str, readable_date: str) -> Dict[str, Any]:
    """
    Extract transaction details from SMS body text using regex patterns
    
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
    
    # Pattern 1: Received money
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
    
    # Pattern 2: Sent/Transferred money
    transfer_pattern = r"(\d+(?:,\d+)*) RWF transferred to ([^(]+)\s*\((\d+)\).*Fee was: (\d+(?:,\d+)*) RWF.*New balance: (\d+(?:,\d+)*) RWF"
    transfer_match = re.search(transfer_pattern, body)
    if transfer_match:
        transaction["type"] = "SENT"
        transaction["amount"] = float(transfer_match.group(1).replace(',', ''))
        transaction["receiver"] = transfer_match.group(2).strip()
        transaction["fee"] = float(transfer_match.group(4).replace(',', ''))
        transaction["balance"] = float(transfer_match.group(5).replace(',', ''))
        transaction["sender"] = "You"
        return transaction
    
    # Pattern 3: Payment to merchant/agent
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
    
    # Pattern 4: Bank deposit
    deposit_pattern = r"A bank deposit of (\d+(?:,\d+)*) RWF.*Your NEW BALANCE\s*:(\d+(?:,\d+)*) RWF"
    deposit_match = re.search(deposit_pattern, body)
    if deposit_match:
        transaction["type"] = "BANK_DEPOSIT"
        transaction["amount"] = float(deposit_match.group(1).replace(',', ''))
        transaction["balance"] = float(deposit_match.group(2).replace(',', ''))
        transaction["sender"] = "Bank"
        transaction["receiver"] = "You"
        return transaction
    
    # Pattern 5: Direct payment debit
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
    
    print(f"💾 Saved {len(transactions)} transactions to {output_path}\n")


if __name__ == "__main__":
    # Parse XML and generate JSON
    xml_file = Path(__file__).parent.parent / "data" / "raw" / "modified_sms_v2.xml"
    output_file = Path(__file__).parent.parent / "data" / "processed" / "transactions.json"
    
    if xml_file.exists():
        transactions = parse_xml_file(xml_file)
        save_to_json(transactions, output_file)
        
        # Print summary statistics
        print("📊 Transaction Type Breakdown:")
        types = {}
        for t in transactions:
            types[t['type']] = types.get(t['type'], 0) + 1
        
        for t_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {t_type}: {count}")
        
        print(f"\n✅ XML parsing complete!")
    else:
        print(f"❌ XML file not found at {xml_file}")
