import numpy as np
import random

m = 5 #Liczba serwerów MEC
n = 15 #Liczba zadań do przypisania

#W minizinc I,J to sety 1..m, 1..n, w pythonie to z grubsza range(1, m), range(1,n)

def erlangB(A, N): #docelowo erlang?
    p = 0
    fact = np.math.factorial(N)
    series = [pow(A,i)/np.math.factorial(i) for i in range(0, N+1)]
    return (fact/sum(series))

b = [36,34,38,27,33] #Pojemności dla każdego mec

a = np.asarray([
    8,15,14,23, 8,16, 8,25, 9,17,25,15,10, 8,24,
    15, 7,23,22,11,11,12,10,17,16, 7,16,10,18,22,
    21,20, 6,22,24,10,24, 9,21,14,11,14,11,19,16,
    20,11, 8,14, 9, 5, 6,19,19, 7, 6, 6,13, 9,18,
    8,13,13,13,10,20,25,16,16,17,10,10, 5,12,23]).reshape(m,n)

c = np.asarray([
    17,21,22,18,24,15,20,18,19,18,16,22,24,24,16,
    23,16,21,16,17,16,19,25,18,21,17,15,25,17,24,
    16,20,16,25,24,16,17,19,19,18,20,16,17,21,24,
    19,19,22,22,20,16,19,17,21,19,25,23,25,25,25,
    18,19,15,15,21,25,16,16,23,15,22,17,19,22,24]).reshape(m,n)




used_trial = [-1]
print('Looking for solutions...')
while True:
    while any(i <= 0 for i in used_trial):
        X = np.zeros(shape=(m,n), dtype=int)
        for x in X.T:
            r = random.randint(0,4)
            x[r] = 1
        used_trial = b - (a*X).sum(axis=1)
    used_trial = [-1]
    print(X)
    print((c*X).sum(axis=0)) #koszt per zadanie <- można tu zrobić genetycznie
    obj = (c * X).sum()  # KOSZT
    print(obj)




#Testowe X
# X = [[0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
#     [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]]

obj = (c*X).sum() #KOSZT
used = (a*X).sum(axis=1)
print(a)
print(b)
print(c)
print(X)
print(obj)
print(used)
