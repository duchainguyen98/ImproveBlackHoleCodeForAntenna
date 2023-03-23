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

location = np.random.randint (2, size = (21,29))
cc=str(location)
f = open("D:\yeulaptrinh.txt", "a")
cxxx=[0,21]
# Ghi data vao cuoi file
cv="\nValue "+str(cxxx)+"\n-----------------------------------------------------\n"
f.write(cc)
f.write(cv)

# Dong File
f.close()
# all_st11ars_fitval = [0,0]

# for i in range(len(arr)):
#     all_stars_fitval =np.add(all_stars_fitval,arr[i])
#     R = np.divide(all_stars_fitval,len(arr))
# print(all_stars_fitval)
# print(R)