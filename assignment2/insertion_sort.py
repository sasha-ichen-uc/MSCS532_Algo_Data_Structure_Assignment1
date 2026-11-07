def insertion_sort_decreasing(arr):
    # Iterate through each element starting from the second
    for i in range(1, len(arr)):
        key = arr[i]  # Store the current element to be inserted
        j = i - 1
        # Shift elements that are smaller than key to the right
        # This is the key change from standard insertion sort:
        # we compare with < instead of > to sort in decreasing order
        while j >= 0 and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1
        # Place the key in its correct position
        arr[j + 1] = key
    return arr


if __name__ == "__main__":
    test = [5, 2, 4, 6, 1, 3]
    print("Input:", test)
    result = insertion_sort_decreasing(test)
    print("Sorted (decreasing):", result)
