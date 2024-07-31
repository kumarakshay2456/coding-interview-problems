"""
You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. 
DO NOT allocate another 2D matrix and do the rotation.
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[7,4,1],[8,5,2],[9,6,3]]
Input: matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
Output: [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
"""

from typing import List

class RotateMatrix:
    def transpose_matrix(self, matrix:List[List[int]]):
        total_row = len(matrix)
        for i in range(total_row):
            for j in range(i, total_row):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
                """
                1.	Tuple Packing:
                    •	The right-hand side of the assignment matrix[j][i], matrix[i][j] creates a tuple with the values matrix[j][i] and matrix[i][j].
                    •	For example, if matrix[j][i] is 4 and matrix[i][j] is 2, this creates the tuple (4, 2).
	            2.	Tuple Unpacking:
	                •	The left-hand side matrix[i][j], matrix[j][i] unpacks the tuple and assigns the values back to matrix[i][j] and matrix[j][i] respectively.
	                •	Continuing the example, (4, 2) is unpacked, and matrix[i][j] is set to 4 and matrix[j][i] is set to 2.
                """

        print("transpose matrix is", matrix)
    
    def reverse_matrix(self, matrix:List[List[int]]):
        print("matrix is", matrix)
        for row in matrix:
            n = len(row) - 1
            i = 0
            while n > i:
                row[n], row[i] = row[i], row[n]
                n -= 1
                i = i + 1
            # row.reverse() One line can replace the inside the for loop
    def rotate_matrix(self, matrix:List[List[int]]):
        self.transpose_matrix(matrix)
        self.reverse_matrix(matrix)
        print("Rotate matrix is", matrix)

if __name__ == "__main__":
    RotateMatrix().rotate_matrix([[1,2,3],[4,5,6],[7,8,9]])
    RotateMatrix().rotate_matrix([[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]])