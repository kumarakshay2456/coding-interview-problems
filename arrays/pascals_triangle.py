"""
Given an integer numRows, return the first numRows of Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly above it as shown:

Input: numRows = 5
Output: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]

Example 2:

Input: numRows = 1
Output: [[1]]

"""
from typing import List


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        result = []
        result.append([1])
        if numRows == 1:
            return result
        for i in range(1, numRows):
            change_row = result[i-1]
            dummy_result = []
            for i in range(len(change_row)):
                if i == 0:
                    dummy_result.append(change_row[i])
                else:
                    dummy_result.append(change_row[i-1]+change_row[i])
            dummy_result.append(change_row[len(change_row)-1])
            result.append(dummy_result)
        return result

if __name__ == "__main__":
    print(Solution().generate(3))

        
        