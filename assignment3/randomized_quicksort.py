"""
Assignment 3 Part 1: Randomized Quicksort
MSCS532 - Algorithms and Data Structures

Implements Randomized Quicksort and Deterministic Quicksort,
then benchmarks both on various input distributions.
"""

import random
import time
import sys


# ===================== RANDOMIZED QUICKSORT =====================

def randomized_quicksort(arr):
    """Sort array using quicksort with random pivot selection."""
    if len(arr) <= 1:
        return arr
    arr = arr.copy()
    _rand_qsort(arr, 0, len(arr) - 1)
    return arr


def _rand_qsort(arr, low, high):
    if low < high:
        pivot_idx = randomized_partition(arr, low, high)
        _rand_qsort(arr, low, pivot_idx - 1)
        _rand_qsort(arr, pivot_idx + 1, high)


def randomized_partition(arr, low, high):
    """Pick a random pivot, swap it to end, then partition."""
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
    return partition(arr, low, high)


def partition(arr, low, high):
    """Lomuto partition scheme using last element as pivot."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ===================== DETERMINISTIC QUICKSORT =====================

def deterministic_quicksort(arr):
    """Sort array using quicksort with first element as pivot."""
    if len(arr) <= 1:
        return arr
    arr = arr.copy()
    _det_qsort(arr, 0, len(arr) - 1)
    return arr


def _det_qsort(arr, low, high):
    if low < high:
        pivot_idx = det_partition(arr, low, high)
        _det_qsort(arr, low, pivot_idx - 1)
        _det_qsort(arr, pivot_idx + 1, high)


def det_partition(arr, low, high):
    """Partition using first element as pivot."""
    arr[low], arr[high] = arr[high], arr[low]
    return partition(arr, low, high)


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


def generate_datasets(size):
    """Generate test datasets of given size."""
    rand_data = [random.randint(0, size * 10) for _ in range(size)]
    return {
        "Random":          rand_data,
        "Sorted":          sorted(rand_data),
        "Reverse Sorted":  sorted(rand_data, reverse=True),
        "Repeated":        [random.choice([1, 2, 3, 4, 5]) for _ in range(size)],
    }


def run_benchmarks():
    sizes = [1000, 5000, 10000, 20000]
    sys.setrecursionlimit(200000)

    print(f"{'Algorithm':<25} {'Dataset':<18} {'Size':<10} {'Time (s)':<12}")
    print("-" * 65)

    for size in sizes:
        datasets = generate_datasets(size)
        for name, data in datasets.items():
            rand_t = benchmark(randomized_quicksort, data)
            det_t = benchmark(deterministic_quicksort, data)
            print(f"{'Randomized QSort':<25} {name:<18} {size:<10} {rand_t:<12.6f}")
            print(f"{'Deterministic QSort':<25} {name:<18} {size:<10} {det_t:<12.6f}")
        print()


if __name__ == "__main__":
    print("=" * 65)
    print("  Randomized vs Deterministic Quicksort Comparison")
    print("=" * 65)
    print()
    run_benchmarks()
