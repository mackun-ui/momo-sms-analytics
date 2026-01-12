"""
Transaction categorization module
"""

from typing import Dict, Any


def categorize_transaction(transaction: Dict[str, Any]) -> str:
    """
    Categorize a transaction based on message content
    
    Args:
        transaction: Transaction dictionary
        
    Returns:
        Category string
    """
    # TODO: Implement categorization logic
    return 'unknown'


def add_metadata(transaction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add categorization and metadata to transaction
    
    Args:
        transaction: Transaction dictionary
        
    Returns:
        Transaction with added metadata
    """
    # TODO: Add category and other metadata
    return transaction
