"""
Created on Mon Oct 19 12:12:06 2020
@author: Marc Bodem
Template for Calling CST from Python
- Lossy Load Waveguide (Microwave Studio)
- Parameter Sweep to load several sample points
- change 2 parameters
- Obtain S-Parameter values
"""
import sys

sys.path.append(r"D:\Program Files (x86)\CST Studio Suite 2023\AMD64\python_cst_libraries")
import cst
import cst.interface
import cst.results
import numpy as np
import scipy.stats
import time
import shutil

def Delete_Anten_Pixel(cst_project,x,y,size_antenna,pixel_size):
    par_change1 = 'Component.Delete \"Antenna\"'

    cst_project.modeler.add_to_history( "delete component: Antenna", par_change1 , timeout = None )

def Anten_Pixel(cst_project,x,y,size_antenna_x,size_antenna_y,pixel_size):
    par_change1 = 'With Brick \n'\
                    '.Name \"Pixel_Ant'+str(x)+'_'+str(y)+'\"\n'\
                    '.Component \"Antenna\"\n'\
                    ' .Material \"Copper (annealed)\"\n'\
                    '.Xrange \"'+str((x-size_antenna_x//2)*pixel_size-pixel_size/2)+'\",\"'+str((x-size_antenna_x//2)*pixel_size+pixel_size/2)+'\"\n'\
                    '.Yrange \"'+str((y-size_antenna_y//2)*pixel_size-pixel_size/2)+'\",\"'+str((y-size_antenna_y//2)*pixel_size+pixel_size/2)+'\"\n'\
                    '.Zrange \"0\",\"meta_thick\"\n'\
                    '.Create\n'\
                    'End With'

    cst_project.modeler.add_to_history( "Pixel_Ant"+str(x)+"_"+str(y), par_change1 , timeout = None )

mycst = cst.interface.DesignEnvironment(mode=cst.interface.DesignEnvironment.StartMode.ExistingOrNew)
mycst1 = cst.interface.DesignEnvironment.open_project(mycst,r'E:\Master\Antenna\Anten_pixel.cst')

pixel_size=2
size_x=21
size_y=21
arr = np.random.randint (2, size = (size_x,size_y))
print(arr)
for i in range(len(arr)):
    for j in range(len(arr[i])):
        if(arr[i][j]==1):
           Anten_Pixel(mycst1,i,j,size_x,size_y,2)
        #    print(str(i)+'  '+str(j))


# mycst1.schematic.execute_vba_code(par_change, timeout=None)
# mycst1.modeler.run_solver()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
