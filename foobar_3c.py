def solution(m):
    # the following gaussian estimator has been copied from the following github
    # https://gist.github.com/j9ac9k/6b5cd12aa9d2e5aa861f942b786293b4
    def gauss(A):
        m = len(A)
        assert all([len(row) == m + 1 for row in A[1:]]), "Matrix rows have non-uniform length"
        n = m + 1
        for k in range(m):
            pivots = [abs(A[i][k]) for i in range(k, m)]
            i_max = pivots.index(max(pivots)) + k

            # Check for singular matrix
            assert A[i_max][k] != 0, "Matrix is singular!"

            # Swap rows
            A[k], A[i_max] = A[i_max], A[k]
            for i in range(k + 1, m):
                f = A[i][k] / A[k][k]
                for j in range(k + 1, n):
                    A[i][j] -= A[k][j] * f
                # Fill lower triangular matrix with zeros:
                A[i][k] = 0
        # Solve equation Ax=b for an upper triangular matrix A
        x = []
        for i in range(m - 1, -1, -1):
            x.insert(0, A[i][m] / A[i][i])
            for k in range(i - 1, -1, -1):
                A[k][m] -= A[k][i] * x[0]
        return x
    # original code below
    # helper function which takes in an array and outputs a prob of changing to the next state
    def stochastic_matrix(matrix):
        prob_matrix = []
        for row in matrix:
            prob_array = []
            for ele in row:
              if not all(not ele for ele in row):
                prob_array.append(float(ele)/float(sum(row)))
              else:
                prob_array.append(ele)
            prob_matrix.append(prob_array)
        return prob_matrix
    # https://stackoverflow.com/questions/40269725/trying-to-construct-identity-matrix
    def n_identity(n):
        m = [[0 for x in range(n)] for y in range(n)]
        for i in range(0, n):
            m[i][i] = -1
        return m
    # https://stackoverflow.com/questions/6382705/add-two-matrices-in-python
    def add_matrix(a, b):
        res = [[None for k in range(len(a))] for n in range(len(a))]
        for i in range(len(a)):
            for j in range(len(a[0])):
                res[i][j] = a[i][j] + b[i][j]
        return res

    # we need to condition the matrix before the gaussian estimation is done
    # we need to subtract an identity matrix and then add the pi column
    # using this as a reference:
    # https://stephens999.github.io/fiveMinuteStats/stationary_distribution.html
    def condition_matrix(matrix):
        n_id = n_identity(len(matrix))
        id_sub = add_matrix(matrix, n_id)
        # add pi row
        for row in id_sub:
            row.append(0)
        b = [([1] * (len(matrix)))]
        return id_sub + b


    m_prob = stochastic_matrix(m)
    conditioned_m = condition_matrix(m_prob)
    print(conditioned_m)
    guass_estimation = gauss(conditioned_m)

    return guass_estimation


print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]))
