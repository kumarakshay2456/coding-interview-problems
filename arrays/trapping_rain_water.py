
def get_total_water(arr):
    if len(arr) == 0 or len(arr) == 1:
        return 0
    left_max= 0
    right_max = 0
    start = 0
    end = len(arr) - 1
    total_water = 0
    while start < end :
        if arr[start] < arr[end]:
            if arr[start] > left_max:
                left_max = arr[start]
            else:
                total_water += left_max - arr[start]
            start = start + 1
        else:
            if arr[end] > right_max:
                right_max = arr[end]
            else:
                total_water = total_water + right_max - arr[end]
            end = end - 1
    
    return total_water




if __name__ == '__main__':
    """
    Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

    Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
    Output: 6
    Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

    Example 2:

    Input: height = [4,2,0,3,2,5]
    Output: 9

    """
    arr = [4,2,0,3,2,5]
    print("Total Water is", get_total_water(arr))
