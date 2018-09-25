import sys

g = sys.maxsize

def matrixmult (A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
      print("Cannot multiply the two matrices. Incorrect dimensions.")
      return

    # Create the result matrix
    # Dimensions would be rows_A x cols_B
    C = [[g for row in range(cols_B)] for col in range(rows_A)]
    #print(C)

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                #C[i][j] += A[i][k] * B[k][j]
                C[i][j] = min(C[i][j], A[i][k] + B[k][j])
    return C

def strange(G):
    nodes = len(G)
    A = G
    for i in range(nodes):
        A = matrixmult(G,A)
    return A

A = [[0, 1, 3, g, g, g, g, g],
     [5, 0, 1, 8, g, g, g, g],
     [g, 9, 0, g, 8, g, g, g],
     [g, g, g, 0, g, g, g, g],
     [g, g, 7, g, 0, g, 2, 7],
     [g, 1, g, 4, g, 0, 7, g],
     [g, g, 7, g, g, g, 0, g],
     [g, g, g, g, g, 1, g, 0]]

#R = matrixmult(A,A) # R = A^2
#S = matrixmult(A,R) # S = A^3
#T = matrixmult(A,S) # T = A^4
#print(T)

X = strange(A)
print(X)