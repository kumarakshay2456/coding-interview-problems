def find_container_with_most_water(arr):
    start = 0
    end = len(arr) - 1
    max_area = 0

    while start <= end:
        min_length = min(arr[start], arr[end])
        width = end - start
        area = min_length * width
        max_area = max(max_area, area)
        if arr[start] < arr[end]:
            start = start + 1
        else:
            end = end - 1
    
    return max_area




if __name__ == '__main__':

    """
    You are given an integer array height of length n.

    There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

    Find two lines that together with the x-axis form a container, such that the container contains the most water.

    Return the maximum amount of water a container can store.

    Notice that you may not slant the container.


    Input: height = [1,8,6,2,5,4,8,3,7]
    Output: 49
    Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7].
    In this case, the max area of water (blue section) the container can contain is 49

    Sol - Summary -
    
	•	Use two pointers.
	•	Calculate area between them.
	•	Move the pointer pointing to the shorter line.
	•	Keep track of the maximum area found.    

    """
    arr = [1,8,6,2,5,4,8,3,7]
    print("Max area is", find_container_with_most_water(arr))