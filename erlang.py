import numpy as np
import matplotlib.pyplot as plt
from math import factorial
def ErlangB (E, m):
    InvB = 1.0
    for j in range(1, m+1):
        InvB = 1.0 + InvB * (j/E)
    return (1.0 / InvB)

# array = []
# for a in range(1,300):
#     er = ErlangB(a/120,5)
#     if er < 0.0001:
#         er = 0
#     array.append(er)
#
# print(array)
# plt.plot(array)
# plt.show()

