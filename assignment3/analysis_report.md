# Assignment 3: Algorithm Efficiency and Scalability — Analysis Report

**MSCS532 — Algorithms and Data Structures**

---

## Part 1: Randomized Quicksort

### Algorithm Description

Randomized Quicksort works like standard quicksort but selects the pivot uniformly at random from the current subarray. This randomization eliminates the dependence on input ordering that causes worst-case behavior in deterministic versions.

The implementation uses the Lomuto partition scheme: after selecting a random pivot and swapping it to the end, a single scan partitions elements into those ≤ pivot and those > pivot.

### Average-Case Analysis

Let T(n) be the expected running time on an input of size n. When the pivot lands at position i (0-indexed), the two recursive calls process subarrays of size i and n − i − 1. Since each position is equally likely:

    T(n) = (1/n) * Σ [T(i) + T(n − i − 1)] + O(n)    for i = 0 to n−1

By symmetry, this simplifies to:

    T(n) = (2/n) * Σ T(i) + O(n)    for i = 0 to n−1

Using indicator random variables, define X_ij = 1 if element i and element j are ever compared. Two elements of rank i and j (with i < j) are compared only when one of them is chosen as a pivot before any element between them. The probability of this is 2/(j − i + 1).

The expected total comparisons are:

    E[comparisons] = Σ Σ 2/(j − i + 1)

Substituting k = j − i, the inner sum becomes a harmonic series:

    = Σ_{i} Σ_{k=1}^{n-i} 2/(k + 1)  ≤  Σ_{i} 2 * H_n  =  O(n log n)

where H_n is the n-th harmonic number ≈ ln(n). This confirms the O(n log n) average-case complexity.

### Empirical Comparison

Running both Randomized and Deterministic (first-element pivot) Quicksort:

| Input Type      | Size   | Randomized (s) | Deterministic (s) |
|-----------------|--------|-----------------|--------------------|
| Random          | 10000  | 0.007           | 0.005              |
| Sorted          | 10000  | 0.006           | 0.658              |
| Reverse Sorted  | 10000  | 0.007           | 1.253              |
| Repeated        | 10000  | 0.349           | 0.348              |
| Random          | 20000  | 0.015           | 0.014              |
| Sorted          | 20000  | 0.015           | 2.873              |
| Reverse Sorted  | 20000  | 0.015           | 5.543              |

**Key Observations:**

1. **Sorted / Reverse-Sorted Inputs:** Deterministic quicksort with first-element pivot hits O(n²) worst case because every partition produces maximally unbalanced splits (one side has 0 elements). Randomized quicksort avoids this entirely — its times stay consistent at ~0.015s for n=20000 regardless of input order.

2. **Random Inputs:** Both algorithms perform similarly since random data already provides good pivot choices on average. Deterministic is slightly faster due to the overhead of calling `random.randint()` in the randomized version.

3. **Repeated Elements:** Both variants perform similarly on repeated elements. With only 5 distinct values, the Lomuto partition scheme creates many equal-to-pivot elements on one side, leading to somewhat unbalanced partitions regardless of pivot selection. A three-way partition scheme (Dutch National Flag) would improve performance here.

4. **Scaling:** Deterministic quicksort on sorted data shows roughly 4x slowdown when doubling n (0.658s → 2.873s), consistent with O(n²) growth. Randomized quicksort shows roughly 2x slowdown (0.007s → 0.015s), consistent with O(n log n).

---

## Part 2: Hash Table with Chaining

### Algorithm Description

The hash table uses chaining: each slot holds a linked list (Python list) of key-value pairs. Collisions are handled by appending to the chain at the hashed index.

**Hash Function:** A universal hash function from the Carter-Wegman family:

    h(k) = ((a * k + b) mod p) mod m

where p is a prime (104729), a and b are random integers chosen at initialization, and m is the table size. This provides a collision probability of at most 1/m for any two distinct keys.

### Complexity Analysis

Under simple uniform hashing, each key is equally likely to hash to any slot. With n elements and m slots, the load factor α = n/m.

- **Insert:** O(1) — hash the key and prepend to the chain. If the key already exists, scan the chain first: O(1 + α) expected.
- **Search (successful):** O(1 + α/2) — on average, we scan half the chain.
- **Search (unsuccessful):** O(1 + α) — scan the entire chain at the hashed slot.
- **Delete:** O(1 + α) — search for the key, then remove it.

When α is kept bounded by a constant (e.g., α ≤ 0.75), all operations are O(1) expected time.

### Load Factor and Dynamic Resizing

The load factor directly impacts performance: as α grows, chains get longer and operations slow down. Our implementation maintains efficiency through dynamic resizing:

- **Grow:** When α > 0.75, double the table size and rehash all entries.
- **Shrink:** When α < 0.25 (and size > minimum), halve the table size.

Resizing costs O(n) since every element must be rehashed, but it happens infrequently enough that the amortized cost per operation remains O(1). Specifically, between two doublings, at least n/2 insertions must occur, spreading the O(n) resize cost across those insertions.

New hash parameters (a, b) are chosen on each resize, maintaining the universal hashing guarantee for the new table size.

### Empirical Results

| Operation | n=1000  | n=5000  | n=10000 | n=50000 |
|-----------|---------|---------|---------|---------|
| Insert    | 0.001s  | 0.004s  | 0.008s  | 0.063s  |
| Search    | 0.000s  | 0.001s  | 0.002s  | 0.010s  |
| Delete    | 0.001s  | 0.003s  | 0.007s  | 0.052s  |

Operations scale linearly with n, confirming O(1) per-operation cost. Insert and delete are slightly slower than search due to the overhead of load-factor checks and occasional resizing.

---

## References

- Cormen, T.H., Leiserson, C.E., Rivest, R.L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Carter, J.L., & Wegman, M.N. (1979). Universal Classes of Hash Functions. *Journal of Computer and System Sciences*, 18(2), 143–154.
