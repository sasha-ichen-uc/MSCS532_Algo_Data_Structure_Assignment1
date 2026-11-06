# MSCS532 Assignment 3: Algorithm Efficiency and Scalability

## Overview

This assignment analyzes two algorithms:
1. **Randomized Quicksort** — comparison with deterministic quicksort across different input distributions
2. **Hash Table with Chaining** — implementation with universal hashing and dynamic resizing

## How to Run

```bash
# Randomized Quicksort benchmarks
python3 randomized_quicksort.py

# Hash Table demo and benchmarks
python3 hash_table.py
```

No external dependencies required — uses only Python standard library.

## Summary of Findings

### Randomized Quicksort
- Randomized pivot selection achieves O(n log n) average-case performance regardless of input distribution.
- Deterministic quicksort (first-element pivot) degrades to O(n²) on sorted and reverse-sorted inputs.
- On random data both variants perform similarly, but the randomized version is more consistent overall.
- Arrays with many repeated elements can cause unbalanced partitions in both variants, though randomized selection still avoids worst-case behavior on structured inputs.

### Hash Table with Chaining
- Under simple uniform hashing, insert, search, and delete all run in O(1) expected time when the load factor is bounded.
- Dynamic resizing (doubling at load factor > 0.75, halving at < 0.25) keeps operations efficient as the table grows.
- The universal hash function family reduces collision clustering compared to naive modular hashing.
- Amortized cost of resizing is O(1) per operation since each element is rehashed O(1) times on average.
