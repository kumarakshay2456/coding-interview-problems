def sort_0_1_2_v1(arr = []):
    if not arr or len(arr) == 1:
        return arr
    zero_count = 0
    one_count = 0
    two_count = 0
    for i in arr:
        if i == 0:
            zero_count += 1
        elif i == 1:
            one_count += 1
        else:
            two_count += 1
        
    for i  in range(len(arr)):
        if zero_count > 0:
            arr[i] = 0
            zero_count -= 1
        elif one_count > 0:
            arr[i] = 1
            one_count -= 1
        else:
            arr[i] = 2
    return arr

def sort_0_1_2_v2(arr = []):
    """
    Note: Here in this tutorial we will work based on the value of the mid pointer.

    The steps will be the following:

        First, we will run a loop that will continue until mid <= high.
        There can be three different values of mid pointer i.e. arr[mid]
           1. If arr[mid] == 0, we will swap arr[low] and arr[mid] and will increment both low and mid. Now the subarray from index 0 to (low-1) only contains 0.
            2. If arr[mid] == 1, we will just increment the mid pointer and then the index (mid-1) will point to 1 as it should according to the rules.
            3. If arr[mid] == 2, we will swap arr[mid] and arr[high] and will decrement high. Now the subarray from index high+1 to (n-1) only contains 2.
            3. If arr[mid] == 2, we will swap arr[mid] and arr[high] and will decrement high. Now the subarray from index high+1 to (n-1) only contains 2.
            In this step, we will do nothing to the mid-pointer as even after swapping, the subarray from mid to high(after decrementing high) might be unsorted. So, we will check the value of mid again in the next iteration.
        Finally, our array should be sorted.
    
    
    """
    if not arr or len(arr) == 1:
        return arr
    low = 0
    mid = 0
    high = len(arr) - 1
    while mid <= high:
        if arr[mid] == 0:
            temp = arr[mid]
            arr[mid] =  arr[low]
            arr[low] = temp
            mid += 1
            low += 1
        elif arr[mid] == 2:
            temp = arr[mid]
            arr[mid] =  arr[high]
            arr[high] = temp
            high -= 1
        else:
            mid += 1
    
    return arr



if __name__ == '__main__':
    """
    Problem Statement: Given an array consisting of only 0s, 1s, and 2s. 
    Write a program to in-place sort the array without using inbuilt sort functions.  Expected: Single pass-O(N) and constant space

    Example :-
    Input: nums = [2,0,2,1,1,0]
    Output: [0,0,1,1,2,2]

    Input: nums = [2,0,1]
    Output: [0,1,2]

    Input: nums = [0]
    Output: [0]
    """
    arr = [2,0,2,1,1,0]
    print(f"Sort array is -> {sort_0_1_2_v2(arr)}")
    arr = [2,0,1]
    print(f"Sort array is -> {sort_0_1_2_v2(arr)}")
    arr = [1, 0, 2, 1, 0,1,0,1,2,0,1]
    print(f"Sort array is -> {sort_0_1_2_v2(arr)}")
