# api/storage.py
"""
Transaction storage and indexing system.
Provides fast O(1) lookup using dictionary-based storage.
"""

class TransactionStorage:
    """
    Manages transaction data with dictionary-based indexing for fast lookup.
    """
    
    def __init__(self):
        """ Initialize empty transaction storage."""
        self.transactions = {}  # {id: transaction_dict}
        self.next_id = 1
    
    def load_transactions(self, transaction_list):
        """
        Load transactions from a list into dictionary storage.
        
        Args:
            transaction_list: List of transaction dictionaries
        """
        for transaction in transaction_list:
            # Ensure each transaction has an ID
            if 'id' not in transaction:
                transaction['id'] = str(self.next_id)
                self.next_id += 1
            
            trans_id = str(transaction['id'])
            self.transactions[trans_id] = transaction
        
        print(f"Loaded {len(self.transactions)} transactions into storage")
    
    def get_all(self):
        """
        Get all transactions.
        
        Returns:
            List of all transaction dictionaries
        """
        return list(self.transactions.values())
    
    def get_by_id(self, trans_id):
        """
        Fast O(1) lookup of transaction by ID.
        
        Args:
            trans_id: Transaction ID to lookup
            
        Returns:
            Transaction dict if found, None otherwise
        """
        return self.transactions.get(str(trans_id))
    
    def add(self, transaction):
        """
        Add a new transaction to storage.
        
        Args:
            transaction: Transaction dictionary
            
        Returns:
            The transaction ID
        """
        # Generate ID if not provided
        if 'id' not in transaction:
            transaction['id'] = str(self.next_id)
            self.next_id += 1
        
        trans_id = str(transaction['id'])
        self.transactions[trans_id] = transaction
        return trans_id
    
    def update(self, trans_id, updated_data):
        """
        Update an existing transaction.
        
        Args:
            trans_id: Transaction ID to update
            updated_data: Dictionary with updated fields
            
        Returns:
            True if updated, False if transaction not found
        """
        trans_id = str(trans_id)
        if trans_id in self.transactions:
            # Update existing transaction with new data
            self.transactions[trans_id].update(updated_data)
            # Ensure ID doesn't change
            self.transactions[trans_id]['id'] = trans_id
            return True
        return False
    
    def delete(self, trans_id):
        """
        Delete a transaction by ID.
        
        Args:
            trans_id: Transaction ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        trans_id = str(trans_id)
        if trans_id in self.transactions:
            del self.transactions[trans_id]
            return True
        return False
    
    def linear_search(self, trans_id):
        """
        Linear O(n) search through all transactions.
        Used for DSA comparison with dictionary lookup.
        
        Args:
            trans_id: Transaction ID to find
            
        Returns:
            Transaction dict if found, None otherwise
        """
        trans_id = str(trans_id)
        for transaction in self.transactions.values():
            if str(transaction.get('id')) == trans_id:
                return transaction
        return None
    
    def count(self):
        """Return total number of transactions."""
        return len(self.transactions)
