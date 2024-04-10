# [[][][]]
# [[][][]]
# [[][][]]
def Progonka(matrix_A, vector_b):
    size = len(vector_b)
    y = []
    alpha = [
        0,
    ]
    betta = [
        0,
    ]

    A = [
        0,
    ]
    B = [
        0,
    ]
    C = [
        0,
    ]

    for i in range(1, size - 1):
        A.append(matrix_A[i][0])
        C.append(-matrix_A[i][1])
        B.append(matrix_A[i][2])

    alpha.append(0)
    betta.append(vector_b[0])
    for i in range(1, size - 1):
        alpha.append(B[i] / (C[i] - A[i] * alpha[i]))
        betta.append((-vector_b[i] + A[i] * betta[i]) / (C[i] - A[i] * alpha[i]))

    y.append(vector_b[-1])
    for i in range(size - 2, -1, -1):
        y.insert(0, alpha[i - size + 1] * y[0] + betta[i - size + 1])

    return y
