

def set_row_column_as_zero(matrix, row, column, max_row, max_column):
    for i in range(0,max_column):
        matrix[row][i] = 0
    for j in range(0, max_row):
        matrix[j][column] = 0
    return matrix

# Approch 1 -  This will take the space complexcity - T(n) = O(N+M)
def define_matrix(matrix):
    set_zero_martix = []
    max_row = len(matrix)
    max_column = len(matrix[0])
    for row in range(0,max_row):
        for column in range(0,max_column):
            if matrix[row][column] == 0:
                set_zero_martix.append([row, column])
    if set_zero_martix:
        for i in set_zero_martix:
            matrix = set_row_column_as_zero(matrix, row=i[0], column=i[1], max_row=max_row, max_column=max_column)
    return matrix

# Approch 2 -  This will take the space complexcity - T(n) = O(N+M)
def set_zero_matrix(matrix):
    max_row = len(matrix)
    max_column = len(matrix[0])
    is_first_row_zero = 0
    is_first_column_zero = 0


    for row in range(max_row):
        for column in range(max_column):
            if matrix[row][column] == 0:
                # Set the first row and column as zero for marker point
                matrix[row][0] = 0
                matrix[0][column] = 0
                if row == 0:
                    is_first_row_zero = 1
                if column == 0:
                    is_first_column_zero = 1
    
    # Now set the zero based on the first row and column
    for row in range(max_row):
        if matrix[row][0] == 0:
            for column in range(max_column):
                matrix[row][column] = 0

    for column in range(max_column):
        if matrix[0][column] == 0:
            for row in range(max_row):
                matrix[row][column] = 0


    if is_first_row_zero:
        for column in range(max_column):
            matrix[0][column] = 0

    if is_first_column_zero:
        for row in range(max_row):
            matrix[row][0] = 0
        
    return matrix

    

if __name__ == '__main__':
    """
    Problem Statement: Given a matrix if an element in the matrix is 0 then
    you will have to set its entire column and row to 0 and then return the matrix.
    
    Examples 1:

    Input: matrix=[[1,1,1],[1,0,1],[1,1,1]]

    Output: [[1,0,1],[0,0,0],[1,0,1]]   
    
    """
    matrix=[[1,1,1],[1,0,1],[1,1,1]]
    matrix = set_zero_matrix(matrix)
    print("Matrix ", matrix)
    matrix=[[0,1,2,0],[3,4,5,2],[1,3,1,5]]
    matrix = set_zero_matrix(matrix)
    print("Matrix ", matrix)

    # Case where first row will be zero
    matrix=[[1,0,2,1],[3,4,5,2],[1,3,1,5]]
    matrix = set_zero_matrix(matrix)
    print("Matrix ", matrix)

    # Case where first coumn will be zero
    matrix=[[1,1,2,1],[3,0,5,2],[1,3,1,5]]
    matrix = set_zero_matrix(matrix)
    print("Matrix ", matrix)
