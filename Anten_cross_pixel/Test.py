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
import Anten_init


def get_result_antenna():
    project = cst.results.ProjectFile(r"C:\Users\dhai9\AppData\Local\Temp\CSTDE1\Temp\DE6\Untitled_0.cst",allow_interactive=True)
    freq_range = [2,6]
    freq_point=[2.45,5.8]
    results = project.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
    # get frequencies
    freqs = results.get_xdata()
    # print(freqs)
    # get S-Parameter values
    S_Para = results.get_ydata()
    # print(S_Para)
    k=results.length
    print(k)
    S_Paraxxx = results.get_data()
    print(S_Paraxxx)

    # Initialize value list for one MC sample point over all frequency points
    freq_pos = []
    freq = []
    S = []
    SdB = []
    S_real = []
    S_imag = []
    freq_range_pos = ((np.array(freq_point)-freq_range[0])*(results.length)/(freq_range[1]-freq_range[0]))
    print(freq_range_pos)
    # Get results for each freq. point of interest from CST
    for j in range(len(freq_range_pos)):
        freq_pos_j = int(freq_range_pos[j])
        freq_pos.append(freq_pos_j)
        print(freq_pos_j)
        freq_value_j = freqs[freq_pos_j]
        print("freq_value_j"+str(freq_value_j))

        freq.append(freq_value_j)

        S_real_j = S_Para[freq_pos_j].real
        S_real.append(S_real_j)
        print("S_real_j"+str(S_real_j))
        S_imag_j = S_Para[freq_pos_j].imag
        S_imag.append(S_imag_j)
        print("S_imag_j"+str(S_imag_j))
        S_phuc = complex(S_Para[freq_pos_j].real, S_Para[freq_pos_j].imag)
        print("S_phuc"+str(S_phuc))
        S_abs= abs(S_phuc)
        print("S_abs"+str(S_abs))
        S_dB_j_abs = 20 * np.log10(S_abs)
        print("S_dB_j_abs"+str(S_dB_j_abs))

        S_j = np.sqrt(S_real_j ** 2 + S_imag_j ** 2)
        S.append(S_j)

        S_dB_j = 20 * np.log10(S_j)
        SdB.append(S_dB_j)

    print(SdB)
    return SdB
get_result_antenna()
# arr=np.array([[1,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,0,1,0,1,1,0,1,0,1,1,0,1,0]
# ,[1,1,0,0,0,1,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1]
# ,[0,1,1,0,0,1,1,0,1,0,1,1,0,1,0,0,1,1,0,0,0,1,0,1,1,0,0,1,1]
# ,[0,1,0,1,0,1,1,0,1,0,1,1,0,0,1,0,0,0,0,1,0,0,1,1,1,0,0,0,0]
# ,[0,1,0,1,1,0,0,0,1,1,1,0,1,0,1,0,0,1,1,0,0,0,1,1,0,0,1,1,0]
# ,[0,1,0,0,0,1,0,1,1,1,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0]
# ,[0,0,1,1,0,0,1,0,1,1,0,0,0,1,0,0,1,1,0,1,0,0,0,1,1,0,0,0,0]
# ,[1,1,1,0,1,0,0,1,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,1,0,0,1,0,0]
# ,[0,1,1,0,0,1,0,1,1,1,0,1,1,0,1,0,1,0,0,1,0,0,1,1,0,1,0,1,1]
# ,[1,1,1,0,1,1,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,0,0]
# ,[0,1,0,1,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,1,0,1,1,0,1,1,1,1,1]
# ,[0,1,1,0,0,1,1,0,1,0,1,0,0,1,0,1,1,0,1,0,0,0,0,0,1,1,1,1,1]
# ,[1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,0,0,1]
# ,[0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0]
# ,[0,0,1,0,1,0,0,0,1,0,0,1,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1,0,1]
# ,[0,0,0,1,0,1,0,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1,1,0,0,1,1]
# ,[0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,0,0,0,0,1,0,0,1,1,0,1,1,1,0]
# ,[0,0,1,0,0,0,1,0,0,0,0,0,1,1,1,0,1,0,0,1,1,0,1,1,1,1,1,1,1]
# ,[0,0,0,1,0,0,1,0,1,1,0,1,0,0,0,1,1,0,0,1,0,0,1,1,0,0,1,1,0]
# ,[1,0,0,0,0,0,1,0,1,1,1,1,1,0,0,1,0,1,1,0,1,0,1,1,0,1,1,0,0]
# ,[1,0,1,1,0,1,0,1,1,0,1,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,1,1,0]])
# # print (arr)
# # antenna=Anten_cross_pixel.Anten(arr)
# # antenna.run_antenna()
# antenna=BH.Star(arr)