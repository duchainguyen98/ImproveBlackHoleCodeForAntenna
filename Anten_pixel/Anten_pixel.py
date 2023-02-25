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
    def Delete_Anten_Pixel(cst_project):
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
    def run_antenna(self):
        mycst = cst.interface.DesignEnvironment(mode=cst.interface.DesignEnvironment.StartMode.ExistingOrNew)
        self.myproject = mycst.open_project(r'E:\Master\Antenna\Anten_AThang.cst')
        print("Antenna"+str(self.PopX))
        for i in range(len(self.PopX)):
            for j in range(len(self.PopX[i])):
                if(self.PopX[i][j]==1):
                # Anten_Pixel(mycst1,i,j,size_x,size_y,2)
                    print(str(i)+'  '+str(j))
        # Anten_Pixel
        self.myproject.modeler.run_solver()    
    def get_result_antenna(self):
        project = cst.results.ProjectFile(r"E:\Master\Antenna\Anten_AThang.cst",allow_interactive=True)
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
        for j in range(len(freq_range_pos)):
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
        print("Antenna Result"+str(Sdb))
        self.Delete_Anten_Pixel(self.myproject)
        self.myproject.close()
        return Sdb


