def insertion_sort_decreasing(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


if __name__ == "__main__":
    test = [5, 2, 4, 6, 1, 3]
    print("Input:", test)
    result = insertion_sort_decreasing(test)
    print("Sorted (decreasing):", result)
