# Assignment 4: Heap Data Structures — Analysis Report

**MSCS532 — Algorithms and Data Structures**

---

## Part 1: Heapsort

### Algorithm Description

Heapsort works in two phases:
1. **Build Max-Heap:** Rearrange the array into a max-heap using bottom-up construction, starting from the last non-leaf node and calling `max_heapify` on each.
2. **Sort:** Repeatedly swap the root (maximum) with the last unsorted element, shrink the heap by one, and call `max_heapify` on the root to restore the heap property.

### Time Complexity Analysis

**Worst case — O(n log n):**
Building the heap is O(n) (not O(n log n), since most nodes are near the leaves and sift down a short distance). The extraction phase performs n − 1 swaps, each followed by a `max_heapify` call that takes O(log n). Total: O(n) + O(n log n) = O(n log n).

**Average case — O(n log n):**
The extraction phase dominates regardless of input distribution. Each `max_heapify` call traverses at most the height of the heap (⌊log n⌋), so the average case is also O(n log n).

**Best case — O(n log n):**
Even when all elements are equal, `max_heapify` still checks children at each level. The extraction loop still runs n − 1 times, each with O(log n) work. Heapsort does not short-circuit on sorted or uniform input.

**Space complexity:** O(1) auxiliary — heapsort is in-place. The only extra space is a constant number of variables for swapping and index tracking. Recursive `max_heapify` uses O(log n) stack space, but this can be made iterative for O(1).

### Empirical Comparison

| Algorithm   | Distribution   | n=10000 (s) | n=20000 (s) |
|-------------|----------------|-------------|-------------|
| Heapsort    | Random         | 0.013       | 0.029       |
| Quicksort   | Random         | 0.007       | 0.014       |
| Merge Sort  | Random         | 0.009       | 0.019       |
| Heapsort    | Sorted         | 0.014       | 0.030       |
| Quicksort   | Sorted         | 0.006       | 0.013       |
| Merge Sort  | Sorted         | 0.006       | 0.012       |
| Heapsort    | Reverse Sorted | 0.012       | 0.027       |
| Quicksort   | Reverse Sorted | 0.006       | 0.013       |
| Merge Sort  | Reverse Sorted | 0.006       | 0.013       |

**Observations:**

1. All three algorithms scale as O(n log n) — doubling n roughly doubles the time, consistent with linearithmic growth.

2. Heapsort is consistently the slowest of the three. This is because `max_heapify` accesses array elements in a scattered pattern (jumping between parent and child indices), which leads to poor cache utilization compared to the sequential access patterns of merge sort and quicksort.

3. Quicksort is the fastest on all distributions. Its in-place partitioning scans the array sequentially, giving excellent cache locality. The randomized pivot prevents O(n²) degradation on sorted inputs.

4. Merge sort is slightly slower than quicksort due to the overhead of copying subarrays, but it performs consistently across all input types.

5. Heapsort's main advantage is O(1) auxiliary space — it is the only in-place O(n log n) worst-case sort among the three.

---

## Part 2: Priority Queue

### Design Choices

**Data structure:** Array-based binary max-heap (Python list). This is preferred over a pointer-based tree because:
- Parent and child indices are computed with simple arithmetic: parent = (i−1)//2, left = 2i+1, right = 2i+2.
- Contiguous memory gives better cache performance.
- Python lists handle dynamic resizing automatically with amortized O(1) appends.

**Heap type:** Max-heap, so the highest-priority task is always at the root and extracted first.

**Index tracking:** A dictionary maps task_id to its current position in the heap array. This allows `increase_key` and `decrease_key` to locate any task in O(1) instead of scanning the array.

### Task Class

Each `Task` stores:
- `task_id` — unique identifier
- `priority` — numeric priority (higher = more urgent)
- `description` — human-readable label
- `arrival_order` — auto-incremented counter for tracking insertion order

### Operation Analysis

| Operation           | Time Complexity | Explanation |
|---------------------|-----------------|-------------|
| `insert(task)`      | O(log n)        | Append to end, then sift up at most log n levels |
| `extract_max()`     | O(log n)        | Swap root with last element, remove last, sift down at most log n levels |
| `increase_key()`    | O(log n)        | Look up position in O(1) via index dict, increase priority, sift up |
| `decrease_key()`    | O(log n)        | Look up position in O(1) via index dict, decrease priority, sift down |
| `is_empty()`        | O(1)            | Check length of the list |
| `peek()`            | O(1)            | Return heap[0] |

All heap operations are O(log n) because the binary heap has height ⌊log₂ n⌋, and sift-up/sift-down traverse at most one root-to-leaf path.

### Scheduler Simulation

The demo simulates a task scheduler that:
1. Inserts 5 tasks with varying priorities.
2. Shows the highest-priority task via `peek()`.
3. Demonstrates `increase_key` by escalating a low-priority task.
4. Processes all tasks in descending priority order via repeated `extract_max()`.

This models real-world scenarios like OS process scheduling, job queues, and event-driven simulation where tasks must be processed in priority order with dynamic priority updates.

---

## References

- Cormen, T.H., Leiserson, C.E., Rivest, R.L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. Chapters 6–7.
