def A1(A):
    n = len(A)
    if n <= 0:
        return 1
    else:
        for i in range(n):
            print('\n')
            for j in range(n * n):
                print(i, j)
            A1(A[i:n / 2])
            A1(A[n / 2:n])


def fatorial(n):
    if n == 0:
        return 1
    else:
        return n * fatorial(n - 1)

def A2(A):
    n = len(A)
    m = n / 5
    if n <= 0:
        return m
    else:
        x = 0
        for b in A:
            x = x + fatorial(b)
        print(x)
        A2(A[0: m])
        A2(A[m: 2 * m])
        A2(A[2 * m:3 * m])
        A2(A[3 * m:n])
