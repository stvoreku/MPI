import numpy as np
import random
from mpi_chromosome import Chromosome
import matplotlib.pyplot as plt

m = 5 #Liczba serwerów MEC
n = 15 #Liczba zadań do przypisania

#b = [36,34,38,27,33] #Pojemności dla każdego mec
b = [120,120,120,120,120]

def ErlangB (E, m):
    InvB = 1.0
    for j in range(1, m+1):
        InvB = 1.0 + InvB * (j/E)
    return (1.0 / InvB)

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

def cross(parents, num_offspring):
    offsprings_list = []
    #generujemy zadaną liczbę dzieci
    while len(offsprings_list) < num_offspring:
        new_ch = Chromosome(m,n,c)
        new_ch.mix_genes(parents)
        new_ch.mutate()
        if new_ch.feasible(a,b) and new_ch.erlang_feasible(a, len(b), b[0], 0.01):
            offsprings_list.append(new_ch)
    return offsprings_list



used_trial = [-1]
print('Looking for 2 solutions for initial pair')
population = []
while len(population) < 2:
    ch = Chromosome(m,n,c)
    ch.random_feasible(a,b)
    population.append(ch)

print('Got two parents')

cost_array = []
erlang_array = []
flow_array =[]

for i in range(0,1000):
    print(f"Generation {i}")
    print(population)
    offs = cross(population, 3)
    population += offs
    population.sort(key=lambda x: x.cost, reverse=False)
    population = population[0:10] #ograniczamy populacje do najlepszych
    #try_B = sum(b)
    try_usage = sum(population[0].usages(a))
    print(try_usage)
    print(len(b))
    er = ErlangB((try_usage/b[0]), len(b))
    erlang_array.append(er)
    cost_array.append(population[0].cost)
    flow_array.append(try_usage/b[0])

fig, ax = plt.subplots()
plt.figure("1")
ax.plot(erlang_array, label='erlang')
fig.show()
fig, ax = plt.subplots()
plt.figure("2")
ax.plot(cost_array, label='cost')
fig.show()
fig, ax = plt.subplots()
plt.figure("3")
ax.plot(flow_array, label='flows')
fig.show()

