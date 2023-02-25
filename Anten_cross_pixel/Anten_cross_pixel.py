import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2023\AMD64\python_cst_libraries")

import cst
import cst.interface
import cst.results
import numpy as np
import shutil

class Anten:
    def __init__(self, PopX):
        self.PopX = PopX
    def Anten_Pixel(self,i,j,size_antenna_x,size_antenna_y,pixel_size):
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

        self.myproject.modeler.add_to_history( "Pixel_Ant"+str(i)+"_"+str(j), par_change1 , timeout = None )
    def Delete_Anten_Pixel(self):
        par_change1 = 'Component.Delete \"Antenna\"'
        self.myproject.modeler.add_to_history( "delete component: Antenna", par_change1 , timeout = None )
    def run_antenna(self):
        mycst = cst.interface.DesignEnvironment(mode=cst.interface.DesignEnvironment.StartMode.ExistingOrNew)
        self.myproject = mycst.open_project(r'C:\Test\Anten_pixel.cst')
        size_antenna_x=len(self.PopX)
        size_antenna_y=len(self.PopX[1])
        pixel_size=1
        self.PopX[size_antenna_x//2][size_antenna_y//2]=1
        for i in range(len(self.PopX)):
            for j in range(len(self.PopX[i])):
                if(self.PopX[i][j]==1):
                    self.Anten_Pixel(i,j,size_antenna_x,size_antenna_y,pixel_size)
                    # print(str(i)+'  '+str(j))
        # Anten_Pixel
        self.myproject.modeler.run_solver()    
    def get_result_antenna(self):
        project = cst.results.ProjectFile(r"C:\Test\Anten_pixel.cst",allow_interactive=True)
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
        self.Delete_Anten_Pixel()
        self.myproject.save()
        self.myproject.close()
        return Sdb


