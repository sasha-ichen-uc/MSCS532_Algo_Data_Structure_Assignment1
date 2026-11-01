"""
Assignment 2: Divide-and-Conquer Sorting Algorithms
MSCS532 - Algorithms and Data Structures

Implements Merge Sort and Quick Sort, then benchmarks both on
sorted, reverse-sorted, and random datasets to compare
theoretical vs. practical performance.
"""

import random
import time
import sys
import tracemalloc


# ===================== MERGE SORT =====================
# Divide-and-conquer algorithm that splits the array in half,
# recursively sorts each half, then merges them back together.
# Time: O(n log n) in all cases (best, average, worst)
# Space: O(n) auxiliary for the temporary arrays during merge

def merge_sort(arr):
    """Recursively divide the array and merge sorted halves."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    # Divide step: split into two halves
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Conquer step: merge the sorted halves
    return merge(left, right)


def merge(left, right):
    """Merge two sorted arrays into a single sorted array."""
    result = []
    i = j = 0

    # Compare elements from both halves, take the smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ===================== QUICK SORT =====================
# Divide-and-conquer algorithm that selects a pivot element,
# partitions the array around it, then recursively sorts
# the partitions.
# Time: O(n log n) average, O(n^2) worst case (sorted input with bad pivot)
# Space: O(log n) average for recursion stack

def quick_sort(arr):
    """Quick Sort using median-of-three pivot selection."""
    if len(arr) <= 1:
        return arr

    arr = arr.copy()
    _quick_sort_helper(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_helper(arr, low, high):
    """Recursive Quick Sort with in-place partitioning."""
    if low < high:
        # Partition and get the pivot's final index
        pivot_index = partition(arr, low, high)
        # Recursively sort elements before and after pivot
        _quick_sort_helper(arr, low, pivot_index - 1)
        _quick_sort_helper(arr, pivot_index + 1, high)


def partition(arr, low, high):
    """
    Partition using median-of-three pivot selection.
    Picks the median of first, middle, and last elements
    to reduce the chance of worst-case O(n^2) behavior.
    """
    mid = (low + high) // 2

    # Sort low, mid, high to find median
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]

    # Place pivot (median) at high-1
    arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
    pivot = arr[high - 1]

    i = low
    j = high - 1

    while True:
        # Move i right past elements smaller than pivot
        i += 1
        while arr[i] < pivot:
            i += 1
        # Move j left past elements larger than pivot
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            break
        arr[i], arr[j] = arr[j], arr[i]

    # Place pivot in its final sorted position
    arr[i], arr[high - 1] = arr[high - 1], arr[i]
    return i


# ===================== BENCHMARKING =====================

def measure(sort_func, data):
    """Measure execution time and peak memory usage of a sort function."""
    arr = data.copy()

    # Track memory usage
    tracemalloc.start()
    start_time = time.time()

    sort_func(arr)

    end_time = time.time()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    elapsed = end_time - start_time
    return elapsed, peak_memory / 1024  # Convert to KB


def generate_datasets(size):
    """Generate sorted, reverse-sorted, and random datasets."""
    random_data = [random.randint(0, size * 10) for _ in range(size)]
    sorted_data = sorted(random_data)
    reverse_data = sorted(random_data, reverse=True)
    return {
        "Random": random_data,
        "Sorted": sorted_data,
        "Reverse Sorted": reverse_data,
    }


def run_benchmarks():
    """Run benchmarks on multiple dataset sizes and types."""
    sizes = [1000, 5000, 10000, 50000]

    # Increase recursion limit for Quick Sort on large sorted inputs
    sys.setrecursionlimit(200000)

    print(f"{'Algorithm':<15} {'Dataset':<18} {'Size':<10} {'Time (s)':<12} {'Memory (KB)':<12}")
    print("-" * 67)

    results = []

    for size in sizes:
        datasets = generate_datasets(size)

        for dataset_name, data in datasets.items():
            for algo_name, algo_func in [("Merge Sort", merge_sort), ("Quick Sort", quick_sort)]:
                # Run 3 trials and take the average
                times = []
                memories = []
                for _ in range(3):
                    t, m = measure(algo_func, data)
                    times.append(t)
                    memories.append(m)

                avg_time = sum(times) / len(times)
                avg_memory = sum(memories) / len(memories)

                print(f"{algo_name:<15} {dataset_name:<18} {size:<10} {avg_time:<12.6f} {avg_memory:<12.2f}")
                results.append({
                    "algorithm": algo_name,
                    "dataset": dataset_name,
                    "size": size,
                    "time": avg_time,
                    "memory": avg_memory,
                })

        print()

    return results


if __name__ == "__main__":
    print("=" * 67)
    print("  Merge Sort vs Quick Sort — Benchmark Comparison")
    print("=" * 67)
    print()
    results = run_benchmarks()

    print("\nKey Observations:")
    print("-" * 67)
    print("1. Merge Sort performs consistently across all input types")
    print("   due to its O(n log n) guarantee in all cases.")
    print("2. Quick Sort may slow down on sorted/reverse-sorted data")
    print("   depending on pivot selection strategy.")
    print("3. Merge Sort uses more memory (O(n) auxiliary space)")
    print("   compared to Quick Sort's O(log n) stack space.")
    print("4. Quick Sort tends to be faster on random data due to")
    print("   better cache locality from in-place partitioning.")
