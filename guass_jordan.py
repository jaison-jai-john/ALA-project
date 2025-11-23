def gauss_jordan(a, b):
    for i in range(len(b)):
        m1 = a[i][i]
        if m1 == 0:  # the reason we ignore it is because 0 cannot be a pivot
            continue
        # divide the whole row by m1 to make (i,i) into 1
        for j in range(i, len(a[i])):
            a[i][j] = a[i][j] / m1
        print(b[i])
        b[i][0] = b[i][0] / m1

        # make all elements below m1 into 0 using elementary row operations
        for j in range(len(b)):
            if j == i:  # this means its the row with m1 so we ignore it
                continue
            else:
                m2 = a[j][
                    i
                ]  # the reason we take [j,i] as the index is so that we can cycle row wise and not column wise
                for k in range(i, len(a[j])):
                    a[j][k] -= m2 * a[i][k]
                b[j][0] -= m2 * b[i][0]

    sols = []
    for i in range(len(b)):
        sols.append((chr(120 + i), round(b[i][0], 3)))
    print(sols)
    return sols


# gauss_jordan([[1, 2], [3, 4]], [3, 2])
