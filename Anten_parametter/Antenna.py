import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2020\AMD64\python_cst_libraries")

import cst
import cst.interface
import cst.results
import numpy as np
import shutil

class Anten:
    def __init__(self, PopX):
        self.PopX = PopX
    def run_antenna(self):
        self.mycst = cst.interface.DesignEnvironment(mode=cst.interface.DesignEnvironment.StartMode.ExistingOrNew)
        self.myproject = self.mycst.open_project(r'C:\DATA\Master\Antenna\Best_2_45_and_5.8GHz_parametter_2_74mm.cst')
        par_change = 'Sub Main () \n StoreParameter("W0", '+str(self.PopX[0])+')'+\
                        '\n StoreParameter("W1", '+str(self.PopX[1])+')' +\
                        '\n StoreParameter("W2", '+str(self.PopX[2])+')' +\
                        '\n StoreParameter("W3", '+str(self.PopX[3])+')' +\
                        '\n StoreParameter("W4", '+str(self.PopX[4])+')' +\
                        '\n StoreParameter("W5", '+str(self.PopX[5])+')' +\
                        '\nRebuildOnParametricChange (bfullRebuild, bShowErrorMsgBox)\nEnd Sub' 
        resolve_parametter = self.myproject.schematic.execute_vba_code(par_change, timeout=5000)
        if(not resolve_parametter):
            print("Error "+str(resolve_parametter))
        self.mycst.in_quiet_mode = True 
        self.myproject.modeler.full_history_rebuild()
        self.myproject.modeler.run_solver()

    def get_result_antenna(self):
        project_path=self.myproject.filename()
        project = cst.results.ProjectFile(project_path,allow_interactive=True)        
        freq_range = [1.00,8.00]
        freq_point=[2.55,3.75,6.60]
        results = project.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
        # get frequencies
        freqs = results.get_xdata()
        # get S-Parameter values
        S_Para = results.get_ydata()
        # Initialize value list for one MC sample point over all frequency points
        freq = []
        SdB = []
        freq_range_pos = np.round((np.array(freq_point)-freq_range[0])*1000/(freq_range[1]-freq_range[0]))

        # Get results for each freq. point of interest from CST
        for j in range(len(freq_point)):
            freq_pos_j = int(freq_range_pos[j])
            freq_value_j = freqs[freq_pos_j]
            freq.append(freq_value_j)
            S_real_j = S_Para[freq_pos_j].real
            S_imag_j = S_Para[freq_pos_j].imag
            S_j = complex(S_real_j, S_imag_j)
            S_dB_j = 20 * np.log10(abs(S_j))
            SdB.append(S_dB_j)
        return SdB
    def run(self):
        self.run_antenna()
        Sdb=self.get_result_antenna()
        self.myproject.save()        
        self.myproject.close()
        return Sdb


