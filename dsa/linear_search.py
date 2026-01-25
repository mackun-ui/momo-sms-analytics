"""
Linear Search Implementation - O(n) Time Complexity

This module implements a sequential search algorithm that iterates through
each transaction in the list until the target ID is found.

Time Complexity: O(n) - worst case searches entire list
Space Complexity: O(1) - no additional data structures needed
"""

from typing import List, Dict, Any, Optional


def linear_search(transactions: List[Dict[str, Any]], transaction_id: str) -> Optional[Dict[str, Any]]:
    """
    Search for a transaction by ID using linear search
    
    Algorithm:
    1. Iterate through each transaction in the list
    2. Compare each transaction's ID with target ID
    3. Return transaction if match found
    4. Return None if no match after scanning entire list
    
    Args:
        transactions: List of transaction dictionaries
        transaction_id: The ID to search for
        
    Returns:
        Transaction dictionary if found, None otherwise
        
    Example:
        >>> transactions = [{"id": "1", "amount": 100}, {"id": "2", "amount": 200}]
        >>> result = linear_search(transactions, "2")
        >>> print(result)
        {"id": "2", "amount": 200}
    """
    for transaction in transactions:
        if transaction.get('id') == transaction_id:
            return transaction
    
    return None


def linear_search_multiple(transactions: List[Dict[str, Any]], transaction_ids: List[str]) -> List[Optional[Dict[str, Any]]]:
    """
    Search for multiple transactions using linear search
    
    Args:
        transactions: List of transaction dictionaries
        transaction_ids: List of IDs to search for
        
    Returns:
        List of transaction dictionaries (None for not found)
    """
    results = []
    for tid in transaction_ids:
        results.append(linear_search(transactions, tid))
    
    return results
