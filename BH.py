import random
import numpy as np
import matplotlib.pyplot as plt

def black_hole_algorithm(obj_func, lb, ub, dim, N, max_iter):
    X = np.zeros((N, dim))
    for i in range(N):
        for j in range(dim):
            X[i][j] = random.uniform(lb[j], ub[j])
    S = np.zeros(N)
    for i in range(N):
        S[i] = obj_func(X[i, :])
    s_star = min(S)
    x_star = X[np.argmin(S), :]
    for t in range(max_iter):
        for i in range(N):
            if S[i] > s_star:
                X[i, :] = x_star + np.random.uniform(-1, 1, dim) * np.abs(x_star - X[i, :])
                S[i] = obj_func(X[i, :])
                if S[i] < s_star:
                    s_star = S[i]
                    x_star = X[i, :]
    return x_star

# Example objective function
def obj_func(x):
    # Simulate the microstrip antenna performance using the input parameters
    # and calculate the objective function (e.g., return the return loss in dB)
    return x[0]**2 + x[1]**2

lb = [-100, -100]
ub = [100, 100]
dim = 2
N = 20
max_iter = 1000

optimal_solution = black_hole_algorithm(obj_func, lb, ub, dim, N, max_iter)
print("Optimal Solution: ", optimal_solution)
