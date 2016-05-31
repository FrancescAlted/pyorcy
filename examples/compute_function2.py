import pyorcy
import numpy as np
{{cimport cython|p}}

{{@cython.boundscheck(False)|c}}
{{def|p}} {{cdef double|c}} value(
    {{int|c}} i, {{int|c}} j, {{double[:]|c}} price, {{double[:]|c}} amount):
    {{cdef int a, p|c}}
    {{c cdef double v}}
    v = price[i] * amount[j]
    return v

@pyorcy.cythonize #p
def f({{int|c}} n, {{int|p}} m):
    {{cdef int i, j|c}}
    {{cdef double v|c}}
    {{cdef double[:] price|c}}
    {{cdef double[:] amount|c}}
    price = np.linspace(1, 2, n)
    amount = np.linspace(3, 4, m)
    v = 0
    for i in range(n):
        for j in range(m):
            v += value(i, j, price, amount)
    return v
