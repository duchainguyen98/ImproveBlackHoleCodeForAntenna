import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2023\AMD64\python_cst_libraries")
import cst
import cst.interface
import cst.results
import numpy as np
import time
import shutil
import random
import Anten_cross_pixel
import BH 
import Anten_init

# mycst = cst.interface.DesignEnvironment(mode=cst.interface.DesignEnvironment.StartMode.ExistingOrNew)
# myproject = mycst.new_mws()
# anten_init=Anten_init.Anten_init(myproject)
# anten_init.run()

pixel_max_x=21
pixel_max_y=29
location=np.random.randint (2, size = (21,29))
antenna=Anten_cross_pixel.Anten(location)
S11= antenna.run()

