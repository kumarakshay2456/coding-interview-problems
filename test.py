from typing import List

def maximum_sub_array(arr: List, target_sum:int) -> int:
    max_arr = 0
    start = 0
    end = 0
    arr_sum = 0 
    for end in range(len(arr)):
        arr_sum = arr_sum + arr[end]

        if arr_sum == target_sum:
            max_arr = max(max_arr, end - start + 1)
        
        while start <  end and arr_sum > target_sum:
            arr_sum = arr_sum - arr[start]
            start = start + 1
            
    return max_arr
    
if __name__=='__main__':
    arr = [10,5,2,7,1,-10]
    target_sum =15
    print(f"Maximum Subarray with lenght {maximum_sub_array(arr, target_sum)}")

    arr = [-5, 8, -14, 2, 4, 12]
    target_sum = -5
    print(f"Maximum Subarray with lenght {maximum_sub_array(arr, target_sum)}")

    arr = [10, -10, 20, 30]
    target_sum = 5
    print(f"Maximum Subarray with lenght {maximum_sub_array(arr, target_sum)}")