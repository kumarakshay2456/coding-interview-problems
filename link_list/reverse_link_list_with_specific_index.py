# Problem - given-an-array-list-arr-of-integers-and-a-position-m-you-have-to-reverse-the-array-after-that-position

def reverseArray1(arr, m): # First sol
    # Write your code here.
    # return arr[:m + 1] + arr[-1:m: -1]
    total_count = m + 1
    array_len = len(arr)

    while (total_count < array_len):
        a, b = arr[total_count], arr[array_len - 1]
        c = a
        a = b
        b = c
        arr[total_count], arr[array_len - 1] = a, b
        total_count += 1
        array_len -= 1
    return arr


def reverseArray2(arr, m):  # Second smallest soln
    return arr[:m + 1] + arr[-1:m: -1]


arr = reverseArray1(arr=[1, 2, 3, 4, 5, 6, 7], m=7)
print("Array is", arr)
