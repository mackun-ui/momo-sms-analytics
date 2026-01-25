"""
Performance Benchmark Module

Compares the efficiency of linear search vs dictionary lookup
for finding transactions by ID.
"""

import time
import json
import random
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Import from same package
try:
    from .linear_search import linear_search
    from .dict_lookup import create_transaction_dict, dict_lookup
except ImportError:
    # Running as script
    from linear_search import linear_search
    from dict_lookup import create_transaction_dict, dict_lookup


def benchmark_search_methods(transactions: List[Dict[str, Any]], num_searches: int = 100) -> Dict[str, Any]:
    """
    Benchmark linear search vs dictionary lookup
    
    Args:
        transactions: List of all transactions
        num_searches: Number of search operations to perform
        
    Returns:
        Dictionary with benchmark results
    """
    # Prepare test data
    all_ids = [t['id'] for t in transactions]
    test_ids = random.choices(all_ids, k=num_searches)
    
    print(f"\n🔬 Benchmarking with {len(transactions)} transactions...")
    print(f"   Running {num_searches} search operations...\n")
    
    # Benchmark Linear Search
    print("⏱️  Testing Linear Search (O(n))...")
    start_time = time.perf_counter()
    
    for tid in test_ids:
        result = linear_search(transactions, tid)
    
    linear_time = time.perf_counter() - start_time
    linear_avg = linear_time / num_searches
    
    print(f"   ✅ Completed in {linear_time:.6f} seconds")
    print(f"   ⏱️  Average: {linear_avg * 1000:.6f} ms per search\n")
    
    # Benchmark Dictionary Lookup
    print("⏱️  Testing Dictionary Lookup (O(1))...")
    
    # Time dictionary creation (one-time cost)
    dict_create_start = time.perf_counter()
    transaction_dict = create_transaction_dict(transactions)
    dict_create_time = time.perf_counter() - dict_create_start
    
    # Time lookups
    lookup_start = time.perf_counter()
    
    for tid in test_ids:
        result = dict_lookup(transaction_dict, tid)
    
    lookup_time = time.perf_counter() - lookup_start
    lookup_avg = lookup_time / num_searches
    
    total_dict_time = dict_create_time + lookup_time
    
    print(f"   📦 Dictionary creation: {dict_create_time:.6f} seconds (one-time cost)")
    print(f"   ✅ Lookups completed in {lookup_time:.6f} seconds")
    print(f"   ⏱️  Average: {lookup_avg * 1000:.6f} ms per search\n")
    
    # Calculate speedup
    speedup = linear_avg / lookup_avg if lookup_avg > 0 else float('inf')
    
    results = {
        "num_transactions": len(transactions),
        "num_searches": num_searches,
        "linear_search": {
            "total_time": linear_time,
            "average_time": linear_avg,
            "average_time_ms": linear_avg * 1000,
            "complexity": "O(n)"
        },
        "dictionary_lookup": {
            "dict_creation_time": dict_create_time,
            "total_lookup_time": lookup_time,
            "average_time": lookup_avg,
            "average_time_ms": lookup_avg * 1000,
            "complexity": "O(1)",
            "total_time_including_creation": total_dict_time
        },
        "comparison": {
            "speedup_factor": speedup,
            "faster_method": "dictionary_lookup"
        }
    }
    
    print("=" * 60)
    print("📊 BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Dataset Size: {len(transactions)} transactions")
    print(f"Test Searches: {num_searches}\n")
    
    print(f"Linear Search (O(n)):")
    print(f"  Total Time: {linear_time:.6f} s")
    print(f"  Avg Per Search: {linear_avg * 1000:.6f} ms\n")
    
    print(f"Dictionary Lookup (O(1)):")
    print(f"  Dictionary Creation: {dict_create_time:.6f} s (one-time)")
    print(f"  Total Lookup Time: {lookup_time:.6f} s")
    print(f"  Avg Per Search: {lookup_avg * 1000:.6f} ms\n")
    
    print(f"🚀 Speedup: {speedup:.2f}x faster with dictionary lookup!")
    print(f"💡 Time saved per search: {(linear_avg - lookup_avg) * 1000:.6f} ms")
    print("=" * 60)
    
    return results


def save_benchmark_results(results: Dict[str, Any], output_path: Path) -> None:
    """
    Save benchmark results to JSON file
    
    Args:
        results: Benchmark results dictionary
        output_path: Path to output file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to {output_path}")


if __name__ == "__main__":
    # Load transactions
    trans_file = Path(__file__).parent.parent / "data" / "processed" / "transactions.json"
    
    if trans_file.exists():
        with open(trans_file, 'r', encoding='utf-8') as f:
            transactions = json.load(f)
        
        # Run benchmark
        results = benchmark_search_methods(transactions, num_searches=100)
        
        # Save results
        output_file = Path(__file__).parent.parent / "data" / "processed" / "benchmark_results.json"
        save_benchmark_results(results, output_file)
    else:
        print(f"❌ Transactions file not found at {trans_file}")
        print("   Run etl/parse_xml.py first to generate transactions.json")
