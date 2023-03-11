import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2020\AMD64\python_cst_libraries")
import cst
import cst.interface
import cst.results
import numpy as np
import time
import shutil
import random
import Antenna_cross_pixel
import BH 
#
# mycst = cst.interface.DesignEnvironment()
# myproject = cst.interface.DesignEnvironment.open_project(mycst,r'E:\Master\Python_code\ANTENNA\2_4.cst')


# % *************************** %
# % ** ALGORITHM’S VARIABLES ** %
# % *************************** %

num_stars = 20 # size of population
# n=4     # dimension of problem 
max_iter = 20 # number of generations

#---------Boundary-------

pixel_max_x = 21
pixel_max_y = 29

ibh = BH.ImprovedBlackHole(num_stars, pixel_max_x, pixel_max_y, max_iter)
best_star = ibh.run()
# % *********************** %
# % ** CREATE POPULATION ** %
# % *********************** %
print("Improved Black Hole Algorithm: Maximum Optimization")
# print("Max Location: %s" % (max_values_loc))
print("Best Star Location: " + str(best_star.location))
print("Best Star Fitness Value:" + (str(best_star.fitval)))
best_antenna=Antenna_cross_pixel.Anten(best_star.location)
best_antenna.run_antenna()
# print(ObjValue)