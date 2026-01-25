"""
Dictionary Lookup Implementation - O(1) Time Complexity

This module uses Python's built-in dictionary (hash table) for constant-time
lookups by transaction ID.

Time Complexity: 
    - Dictionary creation: O(n) - one-time cost
    - Lookup: O(1) average case - direct hash-based access
Space Complexity: O(n) - stores all transactions in dictionary
"""

from typing import List, Dict, Any, Optional


def create_transaction_dict(transactions: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Create a dictionary indexed by transaction ID for O(1) lookups
    
    Algorithm:
    1. Initialize empty dictionary
    2. Iterate through transactions list once
    3. Use transaction ID as key, full transaction as value
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        Dictionary with transaction IDs as keys
        
    Example:
        >>> transactions = [{"id": "1", "amount": 100}, {"id": "2", "amount": 200}]
        >>> trans_dict = create_transaction_dict(transactions)
        >>> print(trans_dict)
        {"1": {"id": "1", "amount": 100}, "2": {"id": "2", "amount": 200}}
    """
    return {transaction['id']: transaction for transaction in transactions}


def dict_lookup(transaction_dict: Dict[str, Dict[str, Any]], transaction_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a transaction by ID using dictionary lookup
    
    Algorithm:
    1. Hash the transaction_id to find bucket location
    2. Retrieve value directly from hash table
    3. Return transaction or None if not found
    
    Args:
        transaction_dict: Dictionary of transactions (id -> transaction)
        transaction_id: The ID to look up
        
    Returns:
        Transaction dictionary if found, None otherwise
        
    Example:
        >>> trans_dict = {"1": {"id": "1", "amount": 100}}
        >>> result = dict_lookup(trans_dict, "1")
        >>> print(result)
        {"id": "1", "amount": 100}
    """
    return transaction_dict.get(transaction_id)


def dict_lookup_multiple(transaction_dict: Dict[str, Dict[str, Any]], transaction_ids: List[str]) -> List[Optional[Dict[str, Any]]]:
    """
    Retrieve multiple transactions using dictionary lookup
    
    Args:
        transaction_dict: Dictionary of transactions
        transaction_ids: List of IDs to look up
        
    Returns:
        List of transaction dictionaries (None for not found)
    """
    return [transaction_dict.get(tid) for tid in transaction_ids]
