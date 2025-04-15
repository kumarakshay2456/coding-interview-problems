from typing import List

def nextGreaterPermutation(A: List[int]) -> List[int]:
    n = len(A) # size of the array.

    # Step 1: Find the break point:
    ind = -1 # break point
    for i in range(n-2, -1, -1):
        if A[i] < A[i + 1]:
            # index i is the break point
            ind = i
            break

    # If break point does not exist:
    if ind == -1:
        # reverse the whole array:
        A.reverse()
        return A

    # Step 2: Find the next greater element
    #         and swap it with arr[ind]:
    for i in range(n - 1, ind, -1):
        if A[i] > A[ind]:
            A[i], A[ind] = A[ind], A[i]
            break

    # Step 3: reverse the right half:
    A[ind+1:] = reversed(A[ind+1:])

    return A


if __name__ == '__main__':
    """
    Given an array Arr[] of integers, rearrange the numbers of the given array into the 
    lexicographically next greater permutation of numbers.
    If such an arrangement is not possible, 
    it must rearrange to the lowest possible order (i.e., sorted in ascending order).

    Example 1 :

        Input format: Arr[] = {1,3,2}
        Output: Arr[] = {2,1,3}
        Explanation: All permutations of {1,2,3} are {{1,2,3} , {1,3,2}, {2,13} , {2,3,1} , {3,1,2} , {3,2,1}}. 
        So, the next permutation just after {1,3,2} is {2,1,3}.

    Example 2:

        Input format: Arr[] = {3,2,1}
        Output: Arr[] = {1,2,3}
        Explanation: As we see all permutations of {1,2,3}, we find {3,2,1} at the last position. 
        So, we have to return the topmost permutation.
    """
    ans = nextGreaterPermutation([3,2,1])
    for it in ans:
        print(it, end=" ")
    print("/n")
    ans = nextGreaterPermutation([1,3,2])
    for it in ans:
        print(it, end=" ")
  