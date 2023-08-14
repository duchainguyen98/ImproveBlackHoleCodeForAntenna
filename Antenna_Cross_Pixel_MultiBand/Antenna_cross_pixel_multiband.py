import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2020\AMD64\python_cst_libraries")
import cst
import cst.interface
import cst.results
import numpy as np
import shutil
import Anten_init

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
                        'End With\n'
        return par_change1
    def Delete_Anten_Pixel(self):
        par_change1 = 'Component.Delete \"Antenna\"'
        self.myproject.modeler.add_to_history( "delete component: Antenna", par_change1 , timeout = None )

    def Add_Pixel(self,begin_i,begin_j,end_i,end_j):
        pixel_0 = '\"Antenna:Pixel_Ant_'+str(begin_i)+"_"+str(begin_j)+ '\", '
        pixel_add = '\"Antenna:Pixel_Ant_'+str(end_i)+"_"+str(end_j)+ '\"\n'
        par_add1='Solid.Add '+ pixel_0 + pixel_add
        self.par_add+=par_add1
        # return par_add1

    def Pair_array(self,array):
        if len(array) == 1:
            return 0

        # Chia đôi dãy thành hai phần bằng nhau
        begin_pointer=0
        end_pointer=len(array)-1
        mid = round(len(array)/2+0.25)
        left_half = array[:mid]
        while(begin_pointer<end_pointer):
            self.Add_Pixel(array[begin_pointer][0],array[begin_pointer][1],array[end_pointer][0],array[end_pointer][1])
            begin_pointer+=1
            end_pointer-=1
        # Đệ quy gọi hàm trên các phần chia ra
        self.Pair_array(left_half)

    def run_antenna(self):
        self.mycst = cst.interface.DesignEnvironment(mode=cst.interface.DesignEnvironment.StartMode.ExistingOrNew)
        self.myproject = self.mycst.new_mws()
        anten_init=Anten_init.Anten_init(self.myproject)
        anten_init.run()
        size_antenna_x=len(self.PopX)
        size_antenna_y=len(self.PopX[1])
        
        pixel_size=1
        Pop_value_1=[]
        par_change=""
        self.par_add=''
        self.PopX[size_antenna_x//2][size_antenna_y//2]=1
        # par_change=self.Anten_Pixel(size_antenna_x//2,size_antenna_y//2,size_antenna_x,size_antenna_y,pixel_size)
        for i in range(len(self.PopX)):
            for j in range(len(self.PopX[i])):
                # if(i==size_antenna_x//2 and j==size_antenna_y//2):
                #     continue
                if(self.PopX[i][j]==1):
                    position=[i,j]
                    Pop_value_1.append(position)
                    par_change+=self.Anten_Pixel(i,j,size_antenna_x,size_antenna_y,pixel_size)
                    # par_add+=self.Add_Pixel(i,j,size_antenna_x,size_antenna_y)
        self.myproject.modeler.add_to_history( "Pixel_Ant", par_change , timeout = None )
        self.Pair_array(Pop_value_1)
        self.myproject.modeler.add_to_history( "Add Pixel: Antenna", self.par_add , timeout = None )

        # Anten_Pixel
        self.myproject.modeler.run_solver()    
    def get_result_antenna(self):
        project_path=self.myproject.filename()
        project = cst.results.ProjectFile(project_path,allow_interactive=True)
        freq_range = [1,8]
        freq_point=[2.55,3.75]
        # freq_point=[2.45,5.8]
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
        for j in range(len(freq_range_pos)):
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
        print("Antenna Result"+str(Sdb))
        # self.Delete_Anten_Pixel()
        # self.myproject.save()
        self.myproject.close()
        return Sdb


