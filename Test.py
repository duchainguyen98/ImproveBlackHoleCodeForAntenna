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

# arr=np.random.rand(1,2)
# print(len(arr))
# def generate_initial():
#     stars = []
#     for i in range(100):
#         location = np.random.randint (100, size = (1,2))
#         stars.append(location)
#     return stars
# def get_best_star(starsx):
#     best_starx = starsx[0]
#     for i in range(1, len(starsx)):
#         for j in range(len(starsx[i])):
#             if (starsx[i][0][j] > best_starx[0][j]):
#                 break
#         best_starx = starsx[i]
#     return best_starx
# def get_best_starx(starsx):
#     best_star = starsx[0]
#     for i in range(1, len(starsx)):
#         if (starsx[i][0][0] <= best_star[0][0]) and (starsx[i][0][1] <= best_star[0][1]):
#             best_star = starsx[i]
#     return best_star


# starsx=generate_initial()
# print(starsx)

# get_best_starx = get_best_starx(starsx)
# print("dddd",get_best_starx)

# best_star_value = get_best_star(starsx)
# print(best_star_value)
arr2=[-17,-1]
arr1=[-2,-18]
x=np.less_equal(arr2,-10)
y=np.all(np.less_equal(arr2,arr1))
print(x)
print(y)

if arr2<=arr1:
    print('sdasdfasdf')
# all_st11ars_fitval = [0,0]

# for i in range(len(arr)):
#     all_stars_fitval =np.add(all_stars_fitval,arr[i])
#     R = np.divide(all_stars_fitval,len(arr))
# print(all_stars_fitval)
# print(R)