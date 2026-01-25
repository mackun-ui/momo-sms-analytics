"""
DSA Reflection & Analysis
Author: Role A - Data Parsing & DSA Lead

This document explains the efficiency comparison between linear search
and dictionary lookup for transaction retrieval.
"""

# WHY DICTIONARY LOOKUP IS FASTER

## Time Complexity Analysis

### Linear Search - O(n)
- Must iterate through list sequentially
- Compares each transaction ID one by one
- Worst case: Search entire list (n comparisons)
- Average case: Search half the list (n/2 comparisons)
- Best case: First element (1 comparison)

For 1,691 transactions:
- Average comparisons: ~845
- Time per search: 0.063 ms

### Dictionary Lookup - O(1)
- Uses hash table for direct access
- Computes hash of key (transaction ID)
- Jumps directly to memory location
- Constant time regardless of dataset size

For 1,691 transactions:
- Comparisons: 1 (always)
- Time per search: 0.0004 ms
- Speedup: 155x faster!

---

## Benchmark Results

Dataset: 1,691 transactions
Test: 100 random lookups

| Method | Complexity | Total Time | Avg/Search | Comparisons |
|--------|-----------|------------|------------|-------------|
| Linear Search | O(n) | 6.35 ms | 0.063 ms | ~845 avg |
| Dictionary Lookup | O(1) | 0.04 ms | 0.0004 ms | 1 |

**Performance Gain:** 155.25x faster

---

## Why the Difference?

### Linear Search Process:
```
Search for ID="500":
1. Check transaction[0].id == "500"? No
2. Check transaction[1].id == "500"? No
3. Check transaction[2].id == "500"? No
...
500. Check transaction[499].id == "500"? Yes! ✓

Result: 500 comparisons
```

### Dictionary Lookup Process:
```
Search for ID="500":
1. Hash("500") → memory address 0x7f8a2b
2. Access transactions_dict["500"] directly
3. Return transaction ✓

Result: 1 operation
```

---

## Other Data Structures to Consider

### 1. Binary Search Tree (BST)
- **Complexity:** O(log n) for search
- **Pros:** Maintains sorted order, range queries possible
- **Cons:** Requires balanced tree, more complex than dictionary
- **Use case:** When you need ordered traversal

For 1,691 items: ~11 comparisons vs 845 (linear)

### 2. Hash Table with Chaining
- **Complexity:** O(1) average, O(n) worst case
- **Pros:** Handles hash collisions better
- **Cons:** More memory overhead
- **Use case:** When collision rate is high

### 3. Trie (Prefix Tree)
- **Complexity:** O(k) where k = key length
- **Pros:** Excellent for prefix searches, autocomplete
- **Cons:** High memory usage
- **Use case:** Search by partial ID or name prefixes

### 4. B-Tree
- **Complexity:** O(log n)
- **Pros:** Optimized for disk storage, database engines use this
- **Cons:** Complex implementation
- **Use case:** Large datasets that don't fit in memory

### 5. Skip List
- **Complexity:** O(log n) average
- **Pros:** Simpler than BST, probabilistic balancing
- **Cons:** Uses more memory than BST
- **Use case:** Concurrent access scenarios

---

## Recommendation for This API

**Best Choice: Dictionary (Hash Table)**

**Reasons:**
1. ✅ O(1) lookup - fastest possible
2. ✅ Built-in to Python - no extra libraries
3. ✅ Low memory overhead for 1,691 records
4. ✅ Perfect for API GET /transactions/{id} endpoint
5. ✅ No sorting required
6. ✅ Simple implementation

**When to Consider Alternatives:**
- Need sorted results → Use BST or sorted list
- Need range queries → Use BST or database index
- Dataset > 1M records → Consider B-Tree with database
- Need prefix search → Use Trie
- Memory constrained → Use linear search (no extra storage)

---

## Real-World Application

In a production API:
1. **Small datasets (<1000):** Dictionary is perfect
2. **Medium datasets (<100K):** Dictionary + caching layer
3. **Large datasets (>100K):** Database with indexes (B-Tree)
4. **Very large (>1M):** Database sharding + Redis cache

For this assignment with 1,691 transactions:
**Dictionary lookup is the optimal choice!**

---

**Conclusion:**
Dictionary lookup provides the best balance of speed, simplicity, and 
memory efficiency for this use case. The 155x speedup over linear search
demonstrates why choosing the right data structure matters in software engineering.
