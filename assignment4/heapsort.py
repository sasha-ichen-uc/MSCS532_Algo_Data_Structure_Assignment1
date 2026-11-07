"""
Assignment 4: Heapsort Implementation and Comparison
MSCS532 - Algorithms and Data Structures

Implements Heapsort using a max-heap, then benchmarks against
Quicksort and Merge Sort on various input distributions.
"""

import random
import time
import sys


# ===================== HEAPSORT =====================

def heapsort(arr):
    """Sort array in-place using heapsort."""
    n = len(arr)

    # Build max-heap (start from last non-leaf node)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(arr, n, i)

    # Extract elements one by one from the heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        max_heapify(arr, i, 0)


def max_heapify(arr, heap_size, i):
    """Maintain max-heap property at index i."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < heap_size and arr[left] > arr[largest]:
        largest = left
    if right < heap_size and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, heap_size, largest)


# ===================== QUICKSORT (for comparison) =====================

def quicksort(arr, low, high):
    if low < high:
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        p = i + 1
        quicksort(arr, low, p - 1)
        quicksort(arr, p + 1, high)


def quicksort_wrapper(arr):
    a = arr.copy()
    quicksort(a, 0, len(a) - 1)
    return a


# ===================== MERGE SORT (for comparison) =====================

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ===================== BENCHMARKING =====================

def benchmark(sort_func, data, trials=3):
    """Average execution time over multiple trials."""
    times = []
    for _ in range(trials):
        copy = data.copy()
        start = time.time()
        sort_func(copy)
        times.append(time.time() - start)
    return sum(times) / len(times)


def heapsort_wrapper(arr):
    a = arr.copy()
    heapsort(a)
    return a


def generate_datasets(size):
    rand_data = [random.randint(0, size * 10) for _ in range(size)]
    return {
        "Random":         rand_data,
        "Sorted":         sorted(rand_data),
        "Reverse Sorted": sorted(rand_data, reverse=True),
    }


def run_benchmarks():
    sizes = [1000, 5000, 10000, 20000]
    sys.setrecursionlimit(200000)

    algorithms = [
        ("Heapsort",    heapsort_wrapper),
        ("Quicksort",   quicksort_wrapper),
        ("Merge Sort",  merge_sort),
    ]

    print(f"{'Algorithm':<15} {'Dataset':<18} {'Size':<10} {'Time (s)':<12}")
    print("-" * 55)

    for size in sizes:
        datasets = generate_datasets(size)
        for dist_name, data in datasets.items():
            for algo_name, algo_func in algorithms:
                t = benchmark(algo_func, data)
                print(f"{algo_name:<15} {dist_name:<18} {size:<10} {t:<12.6f}")
        print()


if __name__ == "__main__":
    print("=" * 55)
    print("  Heapsort vs Quicksort vs Merge Sort")
    print("=" * 55)
    print()
    run_benchmarks()
