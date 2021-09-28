from fractions import Fraction
from fractions import gcd
from functools import reduce
def solution(m):  
    # I heavily relied on the following website for guidence in writing the Markov Chain solution
    # https://brilliant.org/wiki/absorbing-markov-chains/
    # I also heavily relied on the mat function in the following github
    # https://github.com/ThomIves/MatrixInverse/blob/master/LinearAlgebraPurePython.py
    
    def check_squareness(A):
        """
        Makes sure that a matrix is square
            :param A: The matrix to be checked.
        """
        if len(A) != len(A[0]):
            raise ArithmeticError("Matrix must be square to inverse.")
            
    def determinant(A, total=0):
        indices = list(range(len(A)))   
        if len(A) == 2 and len(A[0]) == 2:
            val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
            return val
        for fc in indices:
            As = copy_matrix(A)
            As = As[1:]
            height = len(As)
            builder = 0
            for i in range(height):
                As[i] = As[i][0:fc] + As[i][fc+1:]
            sign = (-1) ** (fc % 2)
            sub_det = determinant(As)
            total += A[0][fc] * sign * sub_det
        return total
    
    def check_non_singular(A):
        det = determinant(A)
        if det != 0:
            return det
        else:
            raise ArithmeticError("Singular Matrix!")    
    
    def check_matrix_equality(A,B, tol=None):
        """
        Checks the equality of two matrices.
            :param A: The first matrix
            :param B: The second matrix
            :param tol: The decimal place tolerance of the check
            :return: The boolean result of the equality check
        """
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            return False
    
        for i in range(len(A)):
            for j in range(len(A[0])):
                if tol == None:
                    if A[i][j] != B[i][j]:
                        return False
                else:
                    if round(A[i][j],tol) != round(B[i][j],tol):
                        return False
    
        return True    
        
    def zeros_matrix(rows, cols):
        """
        Creates a matrix filled with zeros.
            :param rows: the number of rows the matrix should have
            :param cols: the number of columns the matrix should have

            :return: list of lists that form the matrix
        """
        M = []
        while len(M) < rows:
            M.append([])
            while len(M[-1]) < cols:
                M[-1].append(0.0)

        return M    
    def identity_matrix(n):
        """
        Creates and returns an identity matrix.
            :param n: the square size of the matrix
     
            :return: a square identity matrix
        """
        IdM = zeros_matrix(n, n)
        for i in range(n):
            IdM[i][i] = 1.0
     
        return IdM    
    
    def matrix_addition(A, B):
        """
        Adds two matrices and returns the sum
            :param A: The first matrix
            :param B: The second matrix
     
            :return: Matrix sum
        """
        # Section 1: Ensure dimensions are valid for matrix addition
        rowsA = len(A)
        colsA = len(A[0])
        rowsB = len(B)
        colsB = len(B[0])
        if rowsA != rowsB or colsA != colsB:
            raise ArithmeticError('Matrices are NOT the same size.')
     
        # Section 2: Create a new matrix for the matrix sum
        C = zeros_matrix(rowsA, colsB)
     
        # Section 3: Perform element by element sum
        for i in range(rowsA):
            for j in range(colsB):
                C[i][j] = A[i][j] + B[i][j]
     
        return C
 
    def matrix_subtraction(A, B):
        """
        Subtracts matrix B from matrix A and returns difference
            :param A: The first matrix
            :param B: The second matrix
     
            :return: Matrix difference
        """
        # Section 1: Ensure dimensions are valid for matrix subtraction
        rowsA = len(A)
        colsA = len(A[0])
        rowsB = len(B)
        colsB = len(B[0])
        if rowsA != rowsB or colsA != colsB:
            raise ArithmeticError('Matrices are NOT the same size.')
     
        # Section 2: Create a new matrix for the matrix difference
        C = zeros_matrix(rowsA, colsB)
     
        # Section 3: Perform element by element subtraction
        for i in range(rowsA):
            for j in range(colsB):
                C[i][j] = A[i][j] - B[i][j]
     
        return C    
    
    def transpose(M):
        """
        Returns a transpose of a matrix.
            :param M: The matrix to be transposed

            :return: The transpose of the given matrix
        """
        # Section 1: if a 1D array, convert to a 2D array = matrix
        if not isinstance(M[0], list):
            M = [M]
        # Section 2: Get dimensions
        rows = len(M)
        cols = len(M[0])
        # Section 3: MT is zeros matrix with transposed dimensions
        MT = zeros_matrix(cols, rows)
        # Section 4: Copy values from M to it's transpose MT
        for i in range(rows):
            for j in range(cols):
                MT[j][i] = M[i][j]
        return MT    
    def copy_matrix(M):
        rows = len(M)
        cols = len(M[0])
    
        MC = zeros_matrix(rows, cols)
    
        for i in range(rows):
            for j in range(cols):
                MC[i][j] = M[i][j]
    
        return MC

    def matrix_multiply(A, B):
        """
        Returns the product of the matrix A * B
            :param A: The first matrix - ORDER MATTERS!
            :param B: The second matrix

            :return: The product of the two matrices
        """
        # Section 1: Ensure A & B dimensions are correct for multiplication
        rowsA = len(A)
        colsA = len(A[0])
        rowsB = len(B)
        colsB = len(B[0])
        if colsA != rowsB:
            raise ArithmeticError(
                'Number of A columns must equal number of B rows.')
        # Section 2: Store matrix multiplication in a new matrix
        C = zeros_matrix(rowsA, colsB)
        for i in range(rowsA):
            for j in range(colsB):
                total = 0
                for ii in range(colsA):
                    total += A[i][ii] * B[ii][j]
                C[i][j] = total
        return C

    def invert_matrix(A, tol=None):
        """
        Returns the inverse of the passed in matrix.
            :param A: The matrix to be inversed
     
            :return: The inverse of the matrix A
        """
        # Section 1: Make sure A can be inverted.
        check_squareness(A)
        check_non_singular(A)
     
        # Section 2: Make copies of A & I, AM & IM, to use for row ops
        n = len(A)
        AM = copy_matrix(A)
        I = identity_matrix(n)
        IM = copy_matrix(I)
     
        # Section 3: Perform row operations
        indices = list(range(n)) # to allow flexible row referencing ***
        for fd in range(n): # fd stands for focus diagonal
            fdScaler = 1.0 / AM[fd][fd]
            # FIRST: scale fd row with fd inverse. 
            for j in range(n): # Use j to indicate column looping.
                AM[fd][j] *= fdScaler
                IM[fd][j] *= fdScaler
            # SECOND: operate on all rows except fd row as follows:
            for i in indices[0:fd] + indices[fd+1:]: 
                # *** skip row with fd in it.
                crScaler = AM[i][fd] # cr stands for "current row".
                for j in range(n): 
                    # cr - crScaler * fdRow, but one element at a time.
                    AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                    IM[i][j] = IM[i][j] - crScaler * IM[fd][j]
     
        # Section 4: Make sure IM is an inverse of A with specified tolerance
        if check_matrix_equality(I,matrix_multiply(A,IM),tol):
            return IM
        else:
            raise ArithmeticError("Matrix inverse out of tolerance.")   
            
    # https://stackoverflow.com/questions/37237954/calculate-the-lcm-of-a-list-of-given-numbers-in-python/54597248
    
    def find_lcd(lst):
      lcm = 1
      for i in lst:
        lcm = lcm*i//gcd(lcm, i)
      return lcm        
  
    # below is orginal code used to solve an absorbing markov chain
    
    def coerce_matrix(matrix):
      prob_matrix = []
      i = 0
      j = 0
      prob_end_row = None
      first_check = True
      for row in matrix:
          prob_array = []
          for ele in row:
            if not all(not ele for ele in row):
              prob_array.append(ele / sum(row)) 
            else:
              if first_check == True:
                prob_end_row = matrix.index(row)
                first_check = False
              if i == j:
                prob_array.append(1)
              else:
                prob_array.append(ele)
            j += 1
          j = 0
          i += 1
          prob_matrix.append(prob_array)

      Q_rows = prob_end_row
      Q_col = prob_end_row
      R_rows = prob_end_row
      R_cols = len(matrix) - Q_col
      Q = zeros_matrix(Q_rows, Q_col)
      R = zeros_matrix(R_rows, R_cols)

      for i in range(Q_rows):
        for j in range(Q_col):
          Q[i][j] = prob_matrix[i][j]
      for i in range(R_rows):
        for j in range(R_cols):
          R[i][j] = prob_matrix[i][-j-1]
      return prob_matrix, Q, R    
  
    m_prob, Q, R = coerce_matrix(m)
    N = invert_matrix(matrix_subtraction(identity_matrix(len(Q)),Q),tol=1)
    M = matrix_multiply(N,R)    
    
    output = []
    num_list = []
    den_list = []
    scale_list = []
    scaled_num = []
    output = []
    
    for ele in M[0]:
      frac = Fraction(ele).limit_denominator(1000)
      num_list.append(int(frac.numerator))
      den_list.append(int(frac.denominator))
    lcd = find_lcd(den_list)

    for ele in den_list:
      scale_list.append(lcd/ele)
    
    for i in range(len(num_list)):
      scaled_num.append(int(num_list[i]*scale_list[i]))
    scaled_num.reverse()
    output = scaled_num + [lcd]
    return output