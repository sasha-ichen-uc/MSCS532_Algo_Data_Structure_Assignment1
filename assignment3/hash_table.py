"""
Assignment 3 Part 2: Hash Table with Chaining
MSCS532 - Algorithms and Data Structures

Implements a hash table using chaining for collision resolution
with a universal hash function and dynamic resizing.
"""

import random
import time


class HashTable:
    """Hash table with chaining and dynamic resizing."""

    INITIAL_SIZE = 8
    LOAD_FACTOR_HIGH = 0.75
    LOAD_FACTOR_LOW = 0.25
    MIN_SIZE = 8

    def __init__(self, size=None):
        self.size = size or self.INITIAL_SIZE
        self.count = 0
        self.table = [[] for _ in range(self.size)]
        # Universal hash function parameters
        self._p = 104729  # a prime larger than expected key range
        self._a = random.randint(1, self._p - 1)
        self._b = random.randint(0, self._p - 1)

    def _hash(self, key):
        """Universal hash function: h(k) = ((a*k + b) mod p) mod m."""
        k = hash(key)
        return ((self._a * k + self._b) % self._p) % self.size

    def insert(self, key, value):
        """Insert or update a key-value pair."""
        idx = self._hash(key)
        chain = self.table[idx]

        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return

        chain.append((key, value))
        self.count += 1

        if self.count / self.size > self.LOAD_FACTOR_HIGH:
            self._resize(self.size * 2)

    def search(self, key):
        """Return value for key, or None if not found."""
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Remove a key-value pair. Returns True if found."""
        idx = self._hash(key)
        chain = self.table[idx]

        for i, (k, v) in enumerate(chain):
            if k == key:
                chain.pop(i)
                self.count -= 1
                if (self.size > self.MIN_SIZE
                        and self.count / self.size < self.LOAD_FACTOR_LOW):
                    self._resize(self.size // 2)
                return True
        return False

    def _resize(self, new_size):
        """Rehash all entries into a new table."""
        old_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        # Pick new hash parameters for the new table size
        self._a = random.randint(1, self._p - 1)
        self._b = random.randint(0, self._p - 1)

        for chain in old_table:
            for key, value in chain:
                self.insert(key, value)

    def load_factor(self):
        return self.count / self.size


# ===================== DEMO & BENCHMARKING =====================

def demo():
    """Show basic hash table operations."""
    ht = HashTable()

    print("Inserting key-value pairs...")
    test_data = [("alice", 85), ("bob", 92), ("carol", 78),
                 ("dave", 95), ("eve", 88)]
    for key, val in test_data:
        ht.insert(key, val)
        print(f"  insert({key}, {val})  load_factor={ht.load_factor():.2f}")

    print(f"\nSearch results:")
    for key, _ in test_data:
        print(f"  search({key}) = {ht.search(key)}")
    print(f"  search('frank') = {ht.search('frank')}")

    print(f"\nDeleting 'bob'...")
    ht.delete("bob")
    print(f"  search('bob') = {ht.search('bob')}")
    print(f"  load_factor = {ht.load_factor():.2f}")


def benchmark():
    """Benchmark insert, search, and delete at various sizes."""
    sizes = [1000, 5000, 10000, 50000]

    print(f"\n{'Operation':<12} {'Size':<10} {'Time (s)':<12}")
    print("-" * 34)

    for n in sizes:
        ht = HashTable()
        keys = [f"key_{i}" for i in range(n)]

        # Insert
        start = time.time()
        for i, k in enumerate(keys):
            ht.insert(k, i)
        insert_time = time.time() - start

        # Search
        start = time.time()
        for k in keys:
            ht.search(k)
        search_time = time.time() - start

        # Delete
        start = time.time()
        for k in keys:
            ht.delete(k)
        delete_time = time.time() - start

        print(f"{'Insert':<12} {n:<10} {insert_time:<12.6f}")
        print(f"{'Search':<12} {n:<10} {search_time:<12.6f}")
        print(f"{'Delete':<12} {n:<10} {delete_time:<12.6f}")
        print()


if __name__ == "__main__":
    print("=" * 50)
    print("  Hash Table with Chaining — Demo & Benchmark")
    print("=" * 50)
    print()
    demo()
    print()
    benchmark()
