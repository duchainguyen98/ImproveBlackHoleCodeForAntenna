import sys
sys.path.append(r"D:\Program Files (x86)\CST Studio Suite 2023\AMD64\python_cst_libraries")

import cst
import cst.interface
import cst.results
import numpy as np
import shutil

class Anten:
    def __init__(self, PopX):
        self.PopX = PopX

    def run_antenna(self):
        self.mycst = cst.interface.DesignEnvironment()
        # myproject = cst.interface.DesignEnvironment.open_project(mycst,r'E:\Master\Python_code\ANTENNA\2_4.cst')

        # par_change = 'Sub Main () \nStoreParameter("antx", ’+str(48)+’)\nStoreParameter("groundplane_length",’+str(11)+’)\nRebuildOnParametricChange (bfullRebuild, bShowErrorMsgBox)\nEnd Sub'
        # myproject.schematic.execute_vba_code(par_change, timeout=None)
        # myproject.modeler.run_solver()

    def get_result_antenna(self):
        project = cst.results.ProjectFile(r"E:\Master\Python_code\ANTENNA\2_4.cst",allow_interactive=True)
        freq_range = [2,6]
        freq_point=[2.45,3.5,5.8]
        results = project.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
        # get frequencies
        freqs = results.get_xdata()
        # get S-Parameter values
        S_Para = results.get_ydata()
        # Initialize value list for one MC sample point over all frequency points
        freq_pos = []
        freq = []
        S = []
        SdB = []
        S_real = []
        S_imag = []
        freq_range_pos = (np.array(freq_point)-freq_range[0])*1000/(freq_range[1]-freq_range[0])

        # Get results for each freq. point of interest from CST
        for j in range(len(freq_range)):
            freq_pos_j = round(freq_range_pos[j])
            freq_pos.append(freq_pos_j)

            freq_value_j = freqs[freq_pos_j]
            freq.append(freq_value_j)

            S_real_j = S_Para[freq_pos_j].real
            S_real.append(S_real_j)

            S_imag_j = S_Para[freq_pos_j].imag
            S_imag.append(S_imag_j)

            S_j = np.sqrt(S_real_j ** 2 + S_imag_j ** 2)
            S.append(S_j)

            S_dB_j = 20 * np.log10(S_j)
            SdB.append(S_dB_j)
        return SdB
    def run(self):
        self.run_antenna()
        Sdb=self.get_result_antenna()
        print('Antenna')
        self.mycst.close()
        return Sdb

