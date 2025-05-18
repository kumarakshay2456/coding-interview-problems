def check_to_reach_last_index(arr):
    maximum_jump = 0
    for i in range(len(arr)):
        if i > maximum_jump:
            return False
        maximum_jump = max(maximum_jump, i + arr[i]) 
    return True
if __name__ == '__main__':
    """
     You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.
    
    Return true if you can reach the last index, or false otherwise.
    
    
    """
    arr = [2,3,1,1,4]
    print("Check Maximum jump", check_to_reach_last_index(arr))
    arr = [3,2,1,0,4]
    print("Check Maximum jump", check_to_reach_last_index(arr))

