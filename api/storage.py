class TransactionStorage:
    """
    Stores all our transactions in a dictionary so we can find them instantly.
    Way better than searching through a list every time!
    """
    
    def __init__(self):
        # Main storage - using a dict because it's O(1) for lookups
        self.transactions = {}
        self.next_id = 1  # Keep track of next available ID
    
    def load_transactions(self, transaction_list):
        """
        Takes a list of transactions and loads them into our dictionary.
        This is where we convert from slow list to fast dict!
        """
        for transaction in transaction_list:
            # Make sure every transaction has an ID
            if 'id' not in transaction:
                transaction['id'] = self.next_id
                self.next_id += 1
            
            # Convert string IDs to integers for consistency
            trans_id = int(transaction['id']) if isinstance(transaction['id'], str) else transaction['id']
            transaction['id'] = trans_id
            
            # Store it in our dictionary - this is the magic part!
            self.transactions[trans_id] = transaction
            
            # Update next_id to avoid conflicts
            if trans_id >= self.next_id:
                self.next_id = trans_id + 1
        
        return len(self.transactions)
    
    def get_all(self):
        """Get all transactions as a list"""
        return list(self.transactions.values())
    
    def get_by_id(self, transaction_id):
        """
        This is the star of the show - O(1) lookup!
        Just give me an ID and I'll find it instantly
        """
        # Convert to int if needed
        if isinstance(transaction_id, str):
            transaction_id = int(transaction_id)
        return self.transactions.get(transaction_id)
    
    def add(self, transaction):
        """Add a new transaction to storage"""
        # Give it an ID if it doesn't have one
        if 'id' not in transaction or transaction['id'] is None:
            transaction['id'] = self.next_id
            self.next_id += 1
        
        # Convert ID to int
        trans_id = int(transaction['id']) if isinstance(transaction['id'], str) else transaction['id']
        transaction['id'] = trans_id
        
        # Save it
        self.transactions[trans_id] = transaction
        return transaction
    
    def update(self, transaction_id, updated_data):
        """Update an existing transaction with new data"""
        # Convert ID to int
        if isinstance(transaction_id, str):
            transaction_id = int(transaction_id)
            
        if transaction_id not in self.transactions:
            return None
        
        # Update the fields
        transaction = self.transactions[transaction_id]
        transaction.update(updated_data)
        # Make sure the ID stays the same
        transaction['id'] = transaction_id
        
        return transaction
    
    def delete(self, transaction_id):
        """Remove a transaction from storage"""
        # Convert ID to int
        if isinstance(transaction_id, str):
            transaction_id = int(transaction_id)
        return self.transactions.pop(transaction_id, None)
    
    def exists(self, transaction_id):
        """Check if a transaction exists"""
        if isinstance(transaction_id, str):
            transaction_id = int(transaction_id)
        return transaction_id in self.transactions
    
    def search_by_field(self, field, value):
        """
        Find all transactions that match a certain field value.
        Like finding all "SENT" transactions or all from a specific sender.
        """
        results = []
        for transaction in self.transactions.values():
            if transaction.get(field) == value:
                results.append(transaction)
        return results
    
    def get_count(self):
        """How many transactions do we have?"""
        return len(self.transactions)
    
    def clear(self):
        """Clear everything - start fresh"""
        self.transactions.clear()
        self.next_id = 1


def linear_search(transaction_list, transaction_id):
    """
    The old-school way - check each transaction one by one.
    This is slow but simple. O(n) means it takes longer as the list grows.
    """
    # Convert ID to int if it's a string
    if isinstance(transaction_id, str):
        transaction_id = int(transaction_id)
    
    for transaction in transaction_list:
        trans_id = transaction.get('id')
        # Handle both string and int IDs
        if isinstance(trans_id, str):
            trans_id = int(trans_id)
        if trans_id == transaction_id:
            return transaction
    return None


def dictionary_lookup(transaction_dict, transaction_id):
    """
    The fast way - go straight to the transaction using the ID as a key.
    O(1) means it's always instant, no matter how many transactions we have!
    """
    # Convert ID to int if needed
    if isinstance(transaction_id, str):
        transaction_id = int(transaction_id)
    return transaction_dict.get(transaction_id)


def compare_search_methods(transactions, search_id):
    """
    Let's race! Linear search vs dictionary lookup.
    Spoiler: dictionary wins every time, especially with lots of data.
    """
    import time
    
    # Convert ID to int for fair comparison
    if isinstance(search_id, str):
        search_id = int(search_id)
    
    # Build a dictionary from the list for comparison
    trans_dict = {}
    for t in transactions:
        trans_id = int(t['id']) if isinstance(t['id'], str) else t['id']
        trans_dict[trans_id] = t
    
    # Test linear search - checking each one
    start = time.perf_counter()
    result_linear = linear_search(transactions, search_id)
    time_linear = time.perf_counter() - start
    
    # Test dictionary lookup - direct access
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


# Create a global storage instance that the API will use
storage = TransactionStorage()
