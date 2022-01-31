import numpy as np
import random

class Chromosome():

    def __init__(self, m, n, c):
        self.X = np.zeros(shape=(m, n), dtype=int)
        self.M = m
        self.N = n
        self.C = c

    def __str__(self):
        return f"{str(self.X)} \n"

    @property
    def cost(self):
        return (self.C * self.X).sum()

    def feasible(self, A, B):
        usage = B - (A * self.X).sum(axis=1)
        return all(i >= 0 for i in usage)

    def from_X(self, X):
        self.X = X

    def random_feasible(self, A, B):
        print("Generating random feasible solution")
        used_trial = [-1]
        while any(i <= 0 for i in used_trial):
            trial_X = np.zeros(shape=(self.M, self.N), dtype=int)
            for x in trial_X.T:
                r = random.randint(0, 4)
                x[r] = 1
            used_trial = B - (A * trial_X).sum(axis=1)
        self.X = trial_X

    def mix_genes(self, parents):
        for i in range(0, len(self.X.T)):
            p_index = random.randint(0,1)
            self.X.T[i] = parents[p_index].X.T[i]
    def mutate(self):
        for i in range(0, len(self.X.T)):
            mut_p = random.randint(0,8)
            if mut_p == 1:
                inte = random.randint(0,4)
                self.X.T[i] = np.roll(self.X.T[i], inte)
    def usages(self, A):
        return (A * self.X).sum(axis=1)

    def __repr__(self):
        return f'{self.cost}'


