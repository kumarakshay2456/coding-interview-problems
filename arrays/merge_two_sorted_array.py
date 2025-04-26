def merge_array(arr1, arr2):
    n = len(arr1)
    m = len(arr2)
    left = n - 1
    right = 0

    # Swap the elements until arr1[left] is smaller than arr2[right]:
    while left >= 0 and right < m:
        if arr1[left] > arr2[right]:
            arr1[left], arr2[right] = arr2[right], arr1[left]
            left -= 1
            right += 1
        else:
            break

    # Sort arr1[] and arr2[] individually:
    arr1.sort()
    arr2.sort()

import math

def next_gap(gap):
    if gap <= 1:
        return 0
    return (gap // 2) + (gap % 2)

def merge_array_v2(arr1, arr2):
    n = len(arr1)
    m = len(arr2)
    gap = next_gap(n + m)

    while gap > 0:
        # Comparing elements in the first array.
        i = 0
        while i + gap < n:
            if arr1[i] > arr1[i + gap]:
                arr1[i], arr1[i + gap] = arr1[i + gap], arr1[i]
            i += 1

        # Comparing elements between both arrays.
        j = gap - n if gap > n else 0
        while i < n and j < m:
            if arr1[i] > arr2[j]:
                arr1[i], arr2[j] = arr2[j], arr1[i]
            i += 1
            j += 1

        # Comparing elements in the second array.
        if j < m:
            j = 0
            while j + gap < m:
                if arr2[j] > arr2[j + gap]:
                    arr2[j], arr2[j + gap] = arr2[j + gap], arr2[j]
                j += 1

        gap = next_gap(gap)



if __name__ == '__main__':
    arr1 = [1,2,3]
    arr2 = [4,5,6]
    n = len(arr1)
    m = len(arr2)
    merge_array(arr1, arr2)
    print("The merged arrays are:")
    print("arr1[] = ", end="")
    for i in range(n):
        print(arr1[i], end=" ")
    print("\narr2[] = ", end="")
    for i in range(m):
        print(arr2[i], end=" ")
    merge_array_v2(arr1, arr2)
    print()
    