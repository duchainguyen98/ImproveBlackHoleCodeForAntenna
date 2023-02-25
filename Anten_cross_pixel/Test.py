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
import Anten_cross_pixel
import BH 
from .studio import *

from tempfile import TemporaryDirectory
from _cst_interface import PCBSApi
import cst.eda.pcb_api as pcb_api
import cst.eda.part_library as part_lib
from cst.eda.pcbs.pi_solver_settings import PISolverSettings


pixel_max_x=21
pixel_max_y=29
mycst = cst.interface.DesignEnvironment(mode=cst.interface.DesignEnvironment.StartMode.ExistingOrNew)
myproject = mycst.open_project(r'E:\Master\Antenna\Anten_pixel.cst')
tmp_dir = TemporaryDirectory()
print(tmp_dir)
import os        
# tmp_plb = os.path.join(tmp_dir.name, "design.plb_lib")
# part_lib.save(tmp_plb)
send_command("_load_parts", {'folder': tmp_dir.name})

