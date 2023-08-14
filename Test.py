import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2020\AMD64\python_cst_libraries")
import cst
import cst.interface
import cst.results
import numpy as np
import time
import shutil
import random
import math

start=[]
for j in range(10):
    start.append([np.random.randint(-20,-1),np.random.randint(-20,-1),np.random.randint(-20,-1)])
print(start)
all_stars_fitval =[0,0,0]
best_star = np.array(start[0])
print(type(best_star))
for i in range(1, len(start)):
    if np.all(np.less_equal(start[i],best_star)):
        best_star = start[i]
print("best_star    "+ str(best_star))
for i in range(len(start)):
    all_stars_fitval =np.add(all_stars_fitval,start[i])
R = np.divide(np.array(best_star),np.array(all_stars_fitval))*3
print("calculate_radius_event_horizon    "+ str(np.divide(np.array(best_star),np.array(all_stars_fitval))))
print("calculate_radius_event_horizon    "+ str(R))
# print(best_star)
# print(start[0])
# x=np.array(best_star)
# y=np.array(start[0])
# distance =(np.subtract(np.array(best_star),np.array(start[0])))
# print(distance)
# distance1 =np.fabs(np.subtract(np.array(best_star),np.array(start[0])))
# print(distance1)

# distance = np.sqrt((best_star-start[0])**2)

