
class TransactionStorage:
    """
    In-memory storage system for transactions using dictionary indexing.
    Provides O(1) lookup time compared to O(n) for linear search.
    """
    
    def __init__(self):
        "Initialize empty storage."
        self.transactions = {}  # Dictionary: {id: transaction}
        self.next_id = 1
    
    def load_transactions(self, transaction_list):
        """
        Load transactions from a list into an indexed dictionary.
        
        Args:
            transaction_list: List of transaction dictionaries
            
        Returns:
            int: Number of transactions loaded
        """
        for transaction in transaction_list:
            # Ensure each transaction has an ID
            if 'id' not in transaction:
                transaction['id'] = self.next_id
                self.next_id += 1
            
            # Store in dictionary for fast lookup
            self.transactions[transaction['id']] = transaction
            
            # Update next_id to be one more than the highest ID
            if transaction['id'] >= self.next_id:
                self.next_id = transaction['id'] + 1
        
        return len(self.transactions)
    
    def get_all(self):
        """
        Retrieve all transactions.
        
        Returns:
            list: List of all transaction dictionaries
        """
        return list(self.transactions.values())
    
    def get_by_id(self, transaction_id):
        """
        Fast O(1) lookup of transaction by ID using dictionary.
        
        Args:
            transaction_id: ID of transaction to retrieve
            
        Returns:
            dict: Transaction dictionary if found, None otherwise
        """
        return self.transactions.get(transaction_id)
    
    def add(self, transaction):
        """
        Add a new transaction to storage.
        
        Args:
            transaction: Transaction dictionary to add
            
        Returns:
            dict: The added transaction with assigned ID
        """
        # Assign new ID if not present
        if 'id' not in transaction or transaction['id'] is None:
            transaction['id'] = self.next_id
            self.next_id += 1
        
        # Store transaction
        self.transactions[transaction['id']] = transaction
        
        return transaction
    
    def update(self, transaction_id, updated_data):
        """
        Update an existing transaction.
        
        Args:
            transaction_id: ID of transaction to update
            updated_data: Dictionary with updated fields
            
        Returns:
            dict: Updated transaction if found, None otherwise
        """
        if transaction_id not in self.transactions:
            return None
        
        # Update transaction fields
        transaction = self.transactions[transaction_id]
        transaction.update(updated_data)
        # Ensure ID doesn't change
        transaction['id'] = transaction_id
        
        return transaction
    
    def delete(self, transaction_id):
        """
        Delete a transaction by ID.
        
        Args:
            transaction_id: ID of transaction to delete
            
        Returns:
            dict: Deleted transaction if found, None otherwise
        """
        return self.transactions.pop(transaction_id, None)
    
    def exists(self, transaction_id):
        """
        Check if a transaction exists.
        
        Args:
            transaction_id: ID to check
            
        Returns:
            bool: True if transaction exists, False otherwise
        """
        return transaction_id in self.transactions
    
    def search_by_field(self, field, value):
        """
        Search transactions by a specific field.
        
        Args:
            field: Field name to search
            value: Value to match
            
        Returns:
            list: List of matching transactions
        """
        results = []
        for transaction in self.transactions.values():
            if transaction.get(field) == value:
                results.append(transaction)
        return results
    
    def get_count(self):
        """
        Get total number of transactions.
        
        Returns:
            int: Number of transactions in storage
        """
        return len(self.transactions)
    
    def clear(self):
        """Clear all transactions from storage"""
        self.transactions.clear()
        self.next_id = 1


def linear_search(transaction_list, transaction_id):
    """
    Linear search implementation - O(n) time complexity.
    Scans through list sequentially to find matching ID.
    
    Args:
        transaction_list: List of transaction dictionaries
        transaction_id: ID to search for
        
    Returns:
        dict: Transaction if found, None otherwise
    """
    for transaction in transaction_list:
        if transaction.get('id') == transaction_id:
            return transaction
    return None


def dictionary_lookup(transaction_dict, transaction_id):
    """
    Dictionary lookup - O(1) time complexity.
    Direct hash table lookup for instant retrieval.
    
    Args:
        transaction_dict: Dictionary of transactions {id: transaction}
        transaction_id: ID to search for
        
    Returns:
        dict: Transaction if found, None otherwise
    """
    return transaction_dict.get(transaction_id)


def compare_search_methods(transactions, search_id):
    """
    Compare efficiency of linear search vs dictionary lookup.
    
    Args:
        transactions: List of transaction dictionaries
        search_id: ID to search for
        
    Returns:
        dict: Results with timing information
    """
    import time
    
    # Build a dictionary for comparison
    trans_dict = {t['id']: t for t in transactions}
    
    # Test linear search
    start = time.perf_counter()
    result_linear = linear_search(transactions, search_id)
    time_linear = time.perf_counter() - start
    
    # Test dictionary lookup
    start = time.perf_counter()
    result_dict = dictionary_lookup(trans_dict, search_id)
    time_dict = time.perf_counter() - start
    
    return {
        'linear_search_time': time_linear,
        'dictionary_lookup_time': time_dict,
        'speedup': time_linear / time_dict if time_dict > 0 else float('inf'),
        'found_linear': result_linear is not None,
        'found_dict': result_dict is not None
    }


# Global storage instance for the API
storage = TransactionStorage()
