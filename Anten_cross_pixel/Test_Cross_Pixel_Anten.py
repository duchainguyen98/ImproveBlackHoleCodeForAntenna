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

def Anten_Pixel(cst_project,i,j,size_antenna_x,size_antenna_y,pixel_size):
    x = (i-size_antenna_x//2)*2*pixel_size+((j-size_antenna_y//2)%2)*pixel_size
    y = (j-size_antenna_y//2)*(3*pixel_size/2)
    par_change1 = 'With Extrude\n'\
                    '\t.Reset\n'\
                    '\t.Name \"Pixel_Ant_'+str(i)+'_'+str(j)+'\"\n'\
                    '\t.Component \"Antenna\"\n'\
                    '\t.Material \"Copper (annealed)\"\n'\
                    '\t.Mode \"Pointlist\"\n'\
                    '\t.Height \"meta_thick\"\n'\
                    '\t.Twist \"0.0\"\n'\
                    '\t.Taper \"0.0\"\n'\
                    '\t.Origin \"0.0\", \"0.0\", \"0.0\"\n'\
                    '\t.Uvector \"1.0\", \"0.0\", \"0.0\"\n'\
                    '\t.Vvector \"0.0\", \"1.0\", \"0.0\"\n'\
                    '\t.Point \"'+str(x-pixel_size)+'\", \"'+str(y+pixel_size/2)+'\"\n'\
                    '\t.LineTo \"'+str(x-pixel_size/2)+'\", \"'+str(y+pixel_size/2)+'\"\n'\
                    '\t.LineTo \"'+str(x-pixel_size/2)+'\", \"'+str(y+pixel_size)+'\"\n'\
                    '\t.LineTo \"'+str(x+pixel_size/2)+'\", \"'+str(y+pixel_size)+'\"\n'\
                    '\t.LineTo \"'+str(x+pixel_size/2)+'\", \"'+str(y+pixel_size/2)+'\"\n'\
                    '\t.LineTo \"'+str(x+pixel_size)+'\", \"'+str(y+pixel_size/2)+'\"\n'\
                    '\t.LineTo \"'+str(x+pixel_size)+'\", \"'+str(y-pixel_size/2)+'\"\n'\
                    '\t.LineTo \"'+str(x+pixel_size/2)+'\", \"'+str(y-pixel_size/2)+'\"\n'\
                    '\t.LineTo \"'+str(x+pixel_size/2)+'\", \"'+str(y-pixel_size)+'\"\n'\
                    '\t.LineTo \"'+str(x-pixel_size/2)+'\", \"'+str(y-pixel_size)+'\"\n'\
                    '\t.LineTo \"'+str(x-pixel_size/2)+'\", \"'+str(y-pixel_size/2)+'\"\n'\
                    '\t.LineTo \"'+str(x-pixel_size)+'\", \"'+str(y-pixel_size/2)+'\"\n'\
                    '\t.Create\n'\
                    'End With'

    cst_project.modeler.add_to_history( "Pixel_Ant"+str(i)+"_"+str(j), par_change1 , timeout = None )

mycst = cst.interface.DesignEnvironment(mode=cst.interface.DesignEnvironment.StartMode.ExistingOrNew)
mycst1 = cst.interface.DesignEnvironment.open_project(mycst,r'E:\Master\Antenna\Anten_pixel.cst')

pixel_size=1

arr = np.random.randint (2, size = (21,29))
size_x=len(arr)
size_y=len(arr[0])
arr[size_x//2][size_y//2]=1
print(size_x)
for i in range(len(arr)):
    for j in range(len(arr[i])):
        if(arr[i][j]==1):
           Anten_Pixel(mycst1,i,j,size_x,size_y,pixel_size)
        #    print(str(i)+'  '+str(j))


# mycst1.schematic.execute_vba_code(par_change, timeout=None)
# mycst1.modeler.run_solver()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
