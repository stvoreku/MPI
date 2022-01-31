import numpy as np

from math import factorial
def ErlangB (E, m):
    InvB = 1.0
    for j in range(1, m+1):
        InvB = 1.0 + InvB * (j/E)
    return (1.0 / InvB)

print(ErlangB(0.1111, 1))

