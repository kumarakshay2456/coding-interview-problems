def find_unsorted_array_length(arr):
    """
    1.	Traverse from left to right:
        Track the maximum so far.
	•	If current number is less than max, it’s out of order → update end.
	2.	Traverse from right to left:
	    Track the minimum so far.
	    If current number is greater than min, it’s out of order → update start.
	3.	The unsorted subarray is between start and end.
    """

    """
    If the array was already sorted, then:
        •	Every number from left to right should be greater than or equal to all previous numbers.
        •	Every number from right to left should be less than or equal to all following numbers.

    So, we can use:
        •	a left-to-right pass to find the last index where an element is smaller than the max so far → end
        •	a right-to-left pass to find the first index where an element is greater than the min so far → start
    """

    length = len(arr)
    maximum_so_far = arr[0]
    minimum_so_far = arr[0]
    end = 0
    start = 0
    for i in range(1, length):
        maximum_so_far = max(maximum_so_far, arr[i])
        if arr[i] < maximum_so_far:
            end = i
    for i in range(length-1, 0, -1):
        minimum_so_far = min(minimum_so_far, arr[i])
        if arr[i] > minimum_so_far:
            start = i
    print(f"Start is {start} and end {end}")
    return end - start + 1



if __name__ == '__main__':

    """
    Given an integer array nums, you need to find one continuous subarray such that 
    if you only sort this subarray in non-decreasing order, then the whole array will be sorted in non-decreasing order.
    Return the shortest such subarray and output its length.
    
    Example 1:

        Input: nums = [2,6,4,8,10,9,15]
        Output: 5
        Explanation: You need to sort [6, 4, 8, 10, 9] in ascending order to make the whole array sorted in ascending order.

    Example 2:

    Input: nums = [1,2,3,4]
    Output: 0

    Example 3:

        Input: nums = [1]
        Output: 0
    """

    arr = [2,6,4,8,10,9,15]
    print("Answer is -> ", find_unsorted_array_length(arr))

