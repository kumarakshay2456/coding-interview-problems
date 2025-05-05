def two_sum_problem(arr, target):
    # [5,25,75]
    start = 0
    end = len(arr) - 1
    while start <= end:
        remaining_sum = target -  arr[end]
        if arr[start] == remaining_sum:
            return start + 1 , end + 1
        
        elif arr[start] > remaining_sum:
            end = end - 1
        else:
            start =  start + 1

def three_sum_problem(arr, target):
    length = len(arr)
    end = length - 1
    for i in range(length - 2):
        start = i + 1
        while start < end:
            current_sum = arr[i] + arr[start] + arr[end]
            if current_sum == target:
                return i+1, start+1, end+1
            if arr[start] > (current_sum - arr[start]):
                end = end - 1
            else:
                start = start + 1
    return 0,0,0



    
if __name__ == '__main__':
    """
    Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, 
    find two numbers such that they add up to a specific target number. 
    Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.

    Return the indices of the two numbers, index1 and index2, added by one as an integer array [index1, index2] of length 2.

    The tests are generated such that there is exactly one solution. You may not use the same element twice.

    Your solution must use only constant extra space
    
    Example 1:

        Input: numbers = [2,7,11,15], target = 9
        Output: [1,2]
        Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

    
    """
    # arr = [2,7,11,15]
    # target = 9
    # print(two_sum_problem(arr, target))
    # arr = [2,3,4]
    # target = 6
    # print(two_sum_problem(arr, target))
    # arr = [-1,0]
    # target = -1
    # print(two_sum_problem(arr, target))
    arr = [5,25,75]
    target = 100
    print(two_sum_problem(arr, target))

    arr = [1, 2, 4, 5, 12]
    target = 21
    print(three_sum_problem(arr, target))

