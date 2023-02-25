import sys
sys.path.append(r"D:\Program Files (x86)\CST Studio Suite 2023\AMD64\python_cst_libraries")
import cst
import cst.interface
import cst.results
import numpy as np
import scipy.stats
import time
import shutil
import random
import math
num_pixels = 40
arr = np.random.randint (2, size = (21,29))

population1 =  np.random.randint (2, size = (6,9))
population2 =  np.random.randint (2, size = (6,9))
print("population1 ",population1)
print("population2 ",population2)
def crossover(parent1, parent2):
    # Chọn ngẫu nhiên một vị trí để cắt
    # cut_pointx = random.randint(0, 5)
    # cut_pointy = random.randint(0, 8)
    cut_pointx = 3
    cut_pointy = 4
    print("cut_pointx ",cut_pointx)
    print("cut_pointy ",cut_pointy)

    parent1cut_point=parent1[:cut_pointx,:cut_pointy]
    print("parent1cut_point ",parent1cut_point)
    parent2cut_point=parent2[:cut_pointx,cut_pointy:]
    print("parent2cut_point ",parent2cut_point)

    # Thực hiện lai ghép bằng cách lấy pixel từ cha hoặc mẹ
    # child1 = parent1[:cut_point] + parent2[cut_point:]
    # child2 = parent2[:cut_point] + parent1[cut_point:]
    # child1 = [*parent1cut_point,*parent2cut_point]
    child1 = parent2
    child1[:cut_pointx,:cut_pointy]=parent1cut_point
    print("child1 ",child1)
    return child1

def crossover():
    # get two random stars
    num_stars = 18 # size of population
    n=4     # dimension of problem
    max_iter = 25 # number of generations

    #---------Boundary-------
    WL=np.zeros((n,1))
    WH = np.zeros((n,1))
    WL[0] = 5
    WH[0] = 7
    WL[1] = 6
    WH[1] = 6.15
    WL[2] = 11
    WH[2] = 14
    WL[3] = 15.5
    WH[3] = 18.5

    min_values_loc = WL
    max_values_loc = WH
    location1 = []
    location2 = []

    for j in range(len(min_values_loc)):
        R = random.random()
        change=float(max_values_loc[j] + R * (max_values_loc[j] - min_values_loc[j]))
        location1.append(change)
    star1=location1
    for j in range(len(min_values_loc)):
        R = random.random()
        change=float(max_values_loc[j] + R * (max_values_loc[j] - min_values_loc[j]))
        location2.append(change)
    star2=location2
    print("star1 ",star1)
    print("star2 ",star2)

    # split points
    s1 = random.randint(0, len(min_values_loc) - 1)
    s2 = random.randint(0, len(min_values_loc) - 1)

    if s1 > s2:
        s1, s2 = s2, s1

    # do crossover
    for i in range(s1, s2 + 1):
        star1[i], star2[i] = star2[i], star1[i]
    print("star1 new",star1)
    print("star2 new",star2)    # return star with higher fitness value
    return star1
crossover()