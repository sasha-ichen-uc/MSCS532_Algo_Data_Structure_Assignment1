# MSCS532 Assignment 4: Heap Data Structures

## Overview

This assignment covers two topics:
1. **Heapsort** — Implementation, analysis, and empirical comparison with Quicksort and Merge Sort.
2. **Priority Queue** — Max-heap based priority queue with a Task class for scheduling simulation.

## How to Run

```bash
# Heapsort benchmarks (compares Heapsort, Quicksort, Merge Sort)
python3 heapsort.py

# Priority queue task scheduler demo
python3 priority_queue.py
```

No external dependencies — uses only Python standard library.

## Summary of Findings

### Heapsort
- Heapsort runs in O(n log n) in all cases (worst, average, best) with O(1) auxiliary space.
- Empirically slower than Quicksort and Merge Sort due to poor cache locality from non-sequential memory access during heapify.
- Main advantage is guaranteed in-place O(n log n) worst-case performance.

### Priority Queue
- Array-based max-heap provides O(log n) insert, extract_max, increase_key, and decrease_key.
- Dictionary-based index tracking enables O(1) lookup for key modification operations.
- Suitable for task scheduling where priorities change dynamically.
