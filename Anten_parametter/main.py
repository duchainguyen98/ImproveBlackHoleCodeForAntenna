import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2020\AMD64\python_cst_libraries")
import cst
import cst.interface
import cst.results
import numpy as np
import time
import shutil
import random
import Antenna 
import ImprovedBlackHole 
#
# mycst = cst.interface.DesignEnvironment()
# myproject = cst.interface.DesignEnvironment.open_project(mycst,r'E:\Master\Python_code\ANTENNA\2_4.cst')


# % *************************** %
# % ** ALGORITHM’S VARIABLES ** %
# % *************************** %

num_stars = 30 # size of population
n=6     # dimension of problem
max_iter = 10 # number of generations

#---------Boundary-------
WL=np.zeros((n,1))
WH = np.zeros((n,1))

WL[0] = 0.200
WH[0] = 3.000
WL[1] = 2.000
WH[1] = 13.120
WL[2] = 1.000
WH[2] = 6.800
WL[3] = 2.000
WH[3] = 7.500
WL[4] = 1.000
WH[4] = 9.760
WL[5] = 0.000
WH[5] = 5.000

min_values_loc = WL
max_values_loc = WH

ibh = ImprovedBlackHole.ImprovedBlackHole(num_stars, min_values_loc, max_values_loc, max_iter)
best_value = ibh.run()
# % *********************** %
# % ** CREATE POPULATION ** %
# % *********************** %
print("Improved Black Hole Algorithm: Maximum Optimization")
print("Improved Black Hole Algorithm: Maximum Optimization")
# print("Max Location: %s" % (max_values_loc))
print("Best Star Location: " + str(best_value.location))
print("Best Star Fitness Value:" + (str(best_value.fitval)))
best_antenna=Antenna.Anten(best_value.location)
best_antenna.run_antenna()
# print(ObjValue)
