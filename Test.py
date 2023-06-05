import sys
# sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2020\AMD64\python_cst_libraries")
# import cst
# import cst.interface
# import cst.results
import numpy as np
import time
import shutil
import random
import math
WL=np.zeros((6,1))
WH = np.zeros((6,1))
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
print(len(min_values_loc))
s1 = random.randint(0, len(min_values_loc) - 2)
print(s1)

# for j in range(len(min_values_loc)):
#     R = random.random()
#     change=float(min_values_loc[j] + R * (max_values_loc[j] - min_values_loc[j]))
#     if(j==2):
#         max_values_loc[len(min_values_loc)-1]=change
#     round_change=round(change,3)

# location1 = []
# location2 = []

# for j in range(len(min_values_loc)):
#         Rand = random.random()
#         change_random_star=float(min_values_loc[j] + Rand * (max_values_loc[j] - min_values_loc[j]))
#         # if(j==2):
#         #         self.max_values_location[4]=change_random_star-0.200
#         round_random_star = round(change_random_star,3)
#         location1.append(round_random_star)
# print(location1)
# for j in range(len(min_values_loc)):
#         Rand = random.random()
#         change_random_star=float(min_values_loc[j] + Rand * (max_values_loc[j] - min_values_loc[j]))
#         # if(j==2):
#         #         self.max_values_location[4]=change_random_star-0.200
#         round_random_star = round(change_random_star,3)
#         location2.append(round_random_star)
# print(location2)
# print(location2[1])
 
# # split points
# s1 = random.randint(0, len(min_values_loc) - 1)
# s2 = random.randint(0, len(min_values_loc) - 1)
# print(s1)
# print(s2)

# if s1 > s2:
#     s1, s2 = s2, s1

# # do crossover
# for i in range(s1, s2 + 1):
#     print("ádasc "+str(i))

#     location1[i], location2[i] = location2[i], location1[i]
# child1=location1
# child2=location2

# print("ssss "+str(child1))
# print("aaaaa"+str(child2))
