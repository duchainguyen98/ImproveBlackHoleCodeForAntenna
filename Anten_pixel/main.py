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
import Anten_pixel 
import BH 


# % *************************** %
# % ** ALGORITHM’S VARIABLES ** %
# % *************************** %

num_stars = 18 # size of population
n=4     # dimension of problem
num_pixels=23 # dimension of problem
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

ibh = ImprovedBlackHole.ImprovedBlackHole(num_stars, min_values_loc, max_values_loc, max_iter)
best_star = ibh.run()
# % *********************** %
# % ** CREATE POPULATION ** %
# % *********************** %
print("Improved Black Hole Algorithm: Maximum Optimization")
print("Max Location: %s" % (max_values_loc))
print("Best Star Location: " + str(best_star.location))
print("Best Star Fitness Value:" + (str(best_star.fitval)))
# print(ObjValue)
