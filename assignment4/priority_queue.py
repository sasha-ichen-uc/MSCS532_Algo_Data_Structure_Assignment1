"""
Assignment 4: Priority Queue using a Max-Heap
MSCS532 - Algorithms and Data Structures

Implements a priority queue backed by a binary max-heap stored
in an array. Includes a Task class for task scheduling simulation.
"""


class Task:
    """Represents a schedulable task with a priority."""

    _counter = 0

    def __init__(self, task_id, priority, description=""):
        self.task_id = task_id
        self.priority = priority
        self.description = description
        Task._counter += 1
        self.arrival_order = Task._counter

    def __repr__(self):
        return f"Task(id={self.task_id}, priority={self.priority}, desc='{self.description}')"


class PriorityQueue:
    """Max-heap priority queue stored as a Python list.

    Array representation is chosen because:
    - Parent/child indices are computed with simple arithmetic (no pointers).
    - Contiguous memory layout gives good cache performance.
    - Python lists handle dynamic resizing automatically.
    """

    def __init__(self):
        self.heap = []
        self._index = {}  # task_id -> position in heap

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self._index[self.heap[i].task_id] = j
        self._index[self.heap[j].task_id] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _sift_up(self, i):
        """Move element up to restore heap property. O(log n)."""
        while i > 0 and self.heap[i].priority > self.heap[self._parent(i)].priority:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _sift_down(self, i):
        """Move element down to restore heap property. O(log n)."""
        n = len(self.heap)
        while True:
            largest = i
            left = self._left(i)
            right = self._right(i)

            if left < n and self.heap[left].priority > self.heap[largest].priority:
                largest = left
            if right < n and self.heap[right].priority > self.heap[largest].priority:
                largest = right

            if largest == i:
                break
            self._swap(i, largest)
            i = largest

    def insert(self, task):
        """Insert a task into the priority queue. O(log n)."""
        self.heap.append(task)
        self._index[task.task_id] = len(self.heap) - 1
        self._sift_up(len(self.heap) - 1)

    def extract_max(self):
        """Remove and return the highest-priority task. O(log n)."""
        if self.is_empty():
            raise IndexError("extract_max from empty priority queue")

        max_task = self.heap[0]
        del self._index[max_task.task_id]

        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._index[last.task_id] = 0
            self._sift_down(0)

        return max_task

    def increase_key(self, task_id, new_priority):
        """Increase the priority of a task. O(log n).

        Raises ValueError if new_priority is not higher.
        """
        if task_id not in self._index:
            raise KeyError(f"Task {task_id} not in queue")

        i = self._index[task_id]
        if new_priority < self.heap[i].priority:
            raise ValueError("New priority is lower than current priority")

        self.heap[i].priority = new_priority
        self._sift_up(i)

    def decrease_key(self, task_id, new_priority):
        """Decrease the priority of a task. O(log n)."""
        if task_id not in self._index:
            raise KeyError(f"Task {task_id} not in queue")

        i = self._index[task_id]
        if new_priority > self.heap[i].priority:
            raise ValueError("New priority is higher than current priority")

        self.heap[i].priority = new_priority
        self._sift_down(i)

    def is_empty(self):
        """Check if the priority queue is empty. O(1)."""
        return len(self.heap) == 0

    def peek(self):
        """Return the highest-priority task without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("peek at empty priority queue")
        return self.heap[0]

    def __len__(self):
        return len(self.heap)


# ===================== DEMO: TASK SCHEDULER =====================

def demo_scheduler():
    """Simulate a simple priority-based task scheduler."""
    pq = PriorityQueue()

    tasks = [
        Task("T1", 3, "Write unit tests"),
        Task("T2", 1, "Update README"),
        Task("T3", 5, "Fix critical bug"),
        Task("T4", 2, "Code review"),
        Task("T5", 4, "Deploy to staging"),
    ]

    print("Inserting tasks:")
    for t in tasks:
        pq.insert(t)
        print(f"  Inserted: {t}")

    print(f"\nPeek (highest priority): {pq.peek()}")

    print("\nIncreasing priority of T2 from 1 to 6...")
    pq.increase_key("T2", 6)
    print(f"  Peek after increase: {pq.peek()}")

    print("\nProcessing tasks in priority order:")
    while not pq.is_empty():
        task = pq.extract_max()
        print(f"  Processing: {task}")


if __name__ == "__main__":
    print("=" * 55)
    print("  Priority Queue — Task Scheduler Demo")
    print("=" * 55)
    print()
    demo_scheduler()
