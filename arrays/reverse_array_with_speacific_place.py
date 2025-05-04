def reverse_place(arr, place):
    if len(arr) == place:
        return arr
    end = len(arr) - 1
    start = place - 1
    while start < end:
        end_value = arr[end]
        arr[end] = arr[start]
        arr[start] = end_value
        end = end - 1
        start += 1
    return arr

if __name__ == '__main__':
    # Problem - given-an-array-list-arr-of-integers-and-a-position-m-you-have-to-reverse-the-array-after-that-position
    a = [2,3,4,5,6,7,7]
    place = 1
    print("Reverse array", reverse_place(a, place))
