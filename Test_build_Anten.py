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

sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2023\AMD64\python_cst_libraries")
import cst
import cst.interface
import cst.results
import numpy as np
import time
import shutil

#set the units
def CstDefineUnits(cst_project):
    # define
    Length = "mm"
    Frequency = "GHz"
    Time = "ns"
    TemperatureUnit = "degC"
    Voltage = "V"
    Current = "A"
    Resistance = "Ohm"
    Conductance = "S"
    Capacitance = "pF"
    Inductance = "nH"

    par_change_units ='\'set the units\n'\
                        'With Units\n'\
                        '\t.SetUnit \"Length\", \"' + Length + '\"\n'\
                        '\t.SetUnit \"Frequency\", \"' + Frequency + '\"\n'\
                        '\t.SetUnit \"Voltage\", \"' + Voltage + '\"\n'\
                        '\t.SetUnit \"Resistance\", \"' + Resistance + '\"\n'\
                        '\t.SetUnit \"Inductance\", \"' + Inductance + '\"\n'\
                        '\t.SetUnit \"Temperature\",  \"' + TemperatureUnit + '\"\n'\
                        '\t.SetUnit \"Time\", \"' + Time + '\"\n'\
                        '\t.SetUnit \"Current\", \"' + Current + '\"\n'\
                        '\t.SetUnit \"Conductance\", \"' + Conductance + '\"\n'\
                        '\t.SetUnit \"Capacitance\", \"' + Capacitance + '\"\n'\
                        'End With\n\n'\
                        'ThermalSolver.AmbientTemperature \"0\"\n\n'\
                        '\'----------------------------------------------------------------------------'
    cst_project.modeler.add_to_history("set the units", par_change_units, timeout=None)
#set the frequency range
def CstDefineFrequencyRange(cst_project,frequency_min,frequency_max):
    # define
    par_change_FrequencyRange = '\'set the frequency range\n' \
                                'Solver.FrequencyRange \"' + str(frequency_min) + '\", \"' + str(frequency_max) + '\"\n'\
                                '\'----------------------------------------------------------------------------'
    cst_project.modeler.add_to_history("set the frequency range", par_change_FrequencyRange, timeout=None)
#set the DrawBox
def CstDrawBox(cst_project):
    par_change_mesh = 'Plot.DrawBox True\n\n'\
                        'With Background\n'\
                        '\t.Epsilon \"1.0\"\n'\
                        '\t.Mu \"1.0\"\n'\
                        '\t.XminSpace \"0.0\"\n'\
                        '\t.XmaxSpace \"0.0\"\n'\
                        '\t.YminSpace \"0.0\"\n'\
                        '\t.YmaxSpace \"0.0\"\n'\
                        '\t.ZminSpace \"0.0\"\n'\
                        '\t.ZmaxSpace \"0.0\"\n'\
                        'End With\n\n'\
                        'With Boundary\n'\
                        '\t.Xmin \"expanded open\"\n'\
                        '\t.Xmax \"expanded open\"\n'\
                        '\t.Ymin \"expanded open\"\n'\
                        '\t.Ymax \"expanded open\"\n'\
                        '\t.Zmin \"expanded open\"\n'\
                        '\t.Zmax \"expanded open\"\n'\
                        '\t.Xsymmetry \"none\"\n'\
                        '\t.Ysymmetry \"none\"\n'\
                        '\t.Zsymmetry \"none\"\n'\
                        'End With'
    cst_project.modeler.add_to_history("set the DrawBox", par_change_mesh, timeout=None)
#set the Mesh
def CstMeshInitiator(cst_project):
    par_change_mesh = '\'optimize mesh settings for planar structures\n\n' \
                        'With Mesh\n' \
                        '\t.MergeThinPECLayerFixpoints \"True\"\n' \
                        '\t.RatioLimit \"20\"\n' \
                        '\t.AutomeshRefineAtPecLines \"True\", \"6\"\n' \
                        '\t.FPBAAvoidNonRegUnite \"True\"\n' \
                        '\t.ConsiderSpaceForLowerMeshLimit \"False\"\n' \
                        '\t.MinimumStepNumber \"5\"\n' \
                        '\t.AnisotropicCurvatureRefinement \"True\"\n' \
                        '\t.AnisotropicCurvatureRefinementFSM \"True\"\n' \
                        'End With\n\n' \
                        'With MeshSettings\n' \
                        '\t.SetMeshType \"Hex\"\n' \
                        '\t.Set \"RatioLimitGeometry\", \"20\"\n' \
                        '\t.Set \"EdgeRefinementOn\", \"1\"\n' \
                        '\t.Set \"EdgeRefinementRatio\", \"6\"\n' \
                        'End With\n\n' \
                        'With MeshSettings\n' \
                        '\t.SetMeshType \"HexTLM\"\n' \
                        '\t.Set \"RatioLimitGeometry\", \"20\"\n' \
                        'End With\n\n' \
                        'With MeshSettings\n' \
                        '\t.SetMeshType \"Tet\"\n' \
                        '\t.Set \"VolMeshGradation\", \"1.5\"\n' \
                        '\t.Set \"SrfMeshGradation\", \"1.5\"\n' \
                        'End With\n\n' \
                        '\'change mesh adaption scheme to energy\n' \
                        '\'\t(planar structures tend to store high energy\n' \
                        '\'\tlocally at edges rather than globally in volume)\n\n'\
                        'MeshAdaption3D.SetAdaptionStrategy \"Energy\"'
    cst_project.modeler.add_to_history("set the Mesh", par_change_mesh, timeout=None)
#switch on FD-TET setting for accurate farfields
def CstFD_TETsetting(cst_project):
    par_change_mesh ='\'switch on FD-TET setting for accurate farfields\n' \
                        'FDSolver.ExtrudeOpenBC \"True\"\n' \
                        'PostProcess1D.ActivateOperation \"vswr\", \"true\"\n' \
                        'PostProcess1D.ActivateOperation \"yz-matrices\", \"true\"\n\n' \
                        'With FarfieldPlot\n'\
	                    '\t.ClearCuts \' lateral=phi, polar=theta\n'\
	                    '\t.AddCut \"lateral\", \"0\", \"1\"\n'\
	                    '\t.AddCut \"lateral\", \"90\", \"1\"\n'\
	                    '\t.AddCut \"polar\", \"90\", \"1\"\n'\
                        'End With\n\n'\
                        '\'----------------------------------------------------------------------------'
    cst_project.modeler.add_to_history("switch on FD-TET setting for accurate farfields", par_change_mesh, timeout=None)

#Dim sDefine As String (can farfile moi phai khai bao)
def CstDimsDefineg(cst_project):
    par_change_mesh ='Dim sDefineAt As String\n'\
                        'sDefineAt = \"2;2.45;6\"\n'\
                        'Dim sDefineAtName As String\n'\
                        'sDefineAtName = \"2;2.45;6\"\n'\
                        'Dim sDefineAtToken As String\n'\
                        'sDefineAtToken = \"f=\"\n'\
                        'Dim aFreq() As String\n'\
                        'aFreq = Split(sDefineAt, \";\")\n'\
                        'Dim aNames() As String\n'\
                        'aNames = Split(sDefineAtName, \";\")\n\n'\
                        'Dim nIndex As Integer\n'\
                        'For nIndex = LBound(aFreq) To UBound(aFreq)\n\n'\
                        'Dim zz_val As String\n'\
                        'zz_val = aFreq (nIndex)\n'\
                        'Dim zz_name As String\n'\
                        'zz_name = sDefineAtToken & aNames (nIndex)\n\n'\
                        '\' Define E-Field Monitors\n'\
                        'With Monitor\n'\
                        '\t.Reset\n'\
                        '\t.Name \"e-field (\"& zz_name &\")\"\n'\
                        '\t.Dimension \"Volume\"\n'\
                        '\t.Domain \"Frequency\"\n'\
                        '\t.FieldType \"Efield\"\n'\
                        '\t.MonitorValue  zz_val\n'\
                        '\t.Create\n'\
                        'End With\n\n'\
                        '\' Define H-Field Monitors\n'\
                        'With Monitor\n'\
                        '\t.Reset\n'\
                        '\t.Name "h-field ("& zz_name &")"\n'\
                        '\t.Dimension "Volume"\n'\
                        '\t.Domain "Frequency"\n'\
                        '\t.FieldType "Hfield"\n'\
                        '\t.MonitorValue  zz_val\n'\
                        '\t.Create\n'\
                        'End With\n\n'\
                        '\' Define Power flow Monitors\n'\
                        'With Monitor\n'\
                        '\t.Reset\n'\
                        '\t.Name "power ("& zz_name &")"\n'\
                        '\t.Dimension "Volume"\n'\
                        '\t.Domain "Frequency"\n'\
                        '\t.FieldType "Powerflow"\n'\
                        '\t.MonitorValue  zz_val\n'\
                        '\t.Create\n'\
                        'End With\n\n'\
                        '\' Define Power loss Monitors\n'\
                        'With Monitor\n'\
                        '\t.Reset\n'\
                        '\t.Name "loss ("& zz_name &")"\n'\
                        '\t.Dimension "Volume"\n'\
                        '\t.Domain "Frequency"\n'\
                        '\t.FieldType "Powerloss"\n'\
                        '\t.MonitorValue  zz_val\n'\
                        '\t.Create\n'\
                        'End With\n\n'\
                        '\' Define Farfield Monitors\n'\
                        'With Monitor\n'\
                        '\t.Reset\n'\
                        '\t.Name "farfield ("& zz_name &")"\n'\
                        '\t.Domain "Frequency"\n'\
                        '\t.FieldType "Farfield"\n'\
                        '\t.MonitorValue  zz_val\n'\
                        '\t.ExportFarfieldSource "False"\n'\
                        '\t.Create\n'\
                        'End With\n\n'\
                        'Next\n\n'\
                        '\'----------------------------------------------------------------------------'

    cst_project.modeler.add_to_history("Dim sDefine As String", par_change_mesh, timeout=None)

#set the solver type
def CstSolverType(cst_project):
    par_change_mesh = 'With MeshSettings\n'\
                        '\t.SetMeshType \"Hex\"\n'\
                        '\t.Set \"Version\", 1%\n'\
                        'End With\n\n'\
                        'With Mesh\n'\
                        '.MeshType "PBA"\n'\
                        'End With\n'\
                        '\'set the solver type\n'\
                        'ChangeSolverType(\"HF Time Domain\")\n\n'\
                        '\'----------------------------------------------------------------------------'
    cst_project.modeler.add_to_history("set the solver type", par_change_mesh, timeout=None)
#set material Copper (annealed)
def CstMaterialeCopper(cst_project):
    par_change_mesh = 'With Material\n'\
                        '\t.Reset\n'\
                        '\t.Name "Copper (annealed)"\n'\
                        '\t.Folder ""\n'\
                        '.FrqType "static"\n'\
                        '.Type "Normal"\n'\
                        '.SetMaterialUnit "Hz", "mm"\n'\
                        '.Epsilon "1"\n'\
                        '.Mu "1.0"\n'\
                        '.Kappa "5.8e+007"\n'\
                        '.TanD "0.0"\n'\
                        '.TanDFreq "0.0"\n'\
                        '.TanDGiven "False"\n'\
                        '.TanDModel "ConstTanD"\n'\
                        '.KappaM "0"\n'\
                        '.TanDM "0.0"\n'\
                        '.TanDMFreq "0.0"\n'\
                        '.TanDMGiven "False"\n'\
                        '.TanDMModel "ConstTanD"\n'\
                        '.DispModelEps "None"\n'\
                        '.DispModelMu "None"\n'\
                        '.DispersiveFittingSchemeEps "Nth Order"\n'\
                        '.DispersiveFittingSchemeMu "Nth Order"\n'\
                        '.UseGeneralDispersionEps "False"\n'\
                        '.UseGeneralDispersionMu "False"\n'\
                        '.FrqType "all"\n'\
                        '.Type "Lossy metal"\n'\
                        '.SetMaterialUnit "GHz", "mm"\n'\
                        '.Mu "1.0"\n'\
                        '.Kappa "5.8e+007"\n'\
                        '.Rho "8930.0"\n'\
                        '.ThermalType "Normal"\n'\
                        '.ThermalConductivity "401.0"\n'\
                        '.SpecificHeat "390", "J/K/kg"\n'\
                        '.MetabolicRate "0"\n'\
                        '.BloodFlow "0"\n'\
                        '.VoxelConvection "0"\n'\
                        '.MechanicsType "Isotropic"\n'\
                        '.YoungsModulus "120"\n'\
                        '.PoissonsRatio "0.33"\n'\
                        '.ThermalExpansionRate "17"\n'\
                        '.Colour "1", "1", "0"\n'\
                        '.Wireframe "False"\n'\
                        '.Reflection "False"\n'\
                        '.Allowoutline "True"\n'\
                        '.Transparentoutline "False"\n'\
                        '.Transparency "0"\n'\
                        '.Create\n'\
                        'End With'

    cst_project.modeler.add_to_history("define material: Copper (annealed)", par_change_mesh, timeout=None)    
#set material FR-4(loss free)
def CstMaterialeFR4(cst_project):
    par_change_mesh = 'With Material\n'\
                        '\t.Reset\n'\
                        '\t.Name "FR-4 (loss free)"\n'\
                        '\t.Folder ""\n'\
                        '.FrqType "all"\n'\
                        '.Type "Normal"\n'\
                        '.SetMaterialUnit "GHz", "mm"\n'\
                        '.Epsilon "4.3"\n'\
                        '.Mu "1.0"\n'\
                        '.Kappa "0.0"\n'\
                        '.TanD "0.0"\n'\
                        '.TanDFreq "0.0"\n'\
                        '.TanDGiven "False"\n'\
                        '.TanDModel "ConstTanD"\n'\
                        '.KappaM "0.0"\n'\
                        '.TanDM "0.0"\n'\
                        '.TanDMFreq "0.0"\n'\
                        '.TanDMGiven "False"\n'\
                        '.TanDMModel "ConstKappa"\n'\
                        '.DispModelEps "None"\n'\
                        '.DispModelMu "None"\n'\
                        '.DispersiveFittingSchemeEps "General 1st"\n'\
                        '.DispersiveFittingSchemeMu "General 1st"\n'\
                        '.UseGeneralDispersionEps "False"\n'\
                        '.UseGeneralDispersionMu "False"\n'\
                        '.Rho "0.0"\n'\
                        '.ThermalType "Normal"\n'\
                        '.ThermalConductivity "0.3"\n'\
                        '.SetActiveMaterial "all"\n'\
                        '.Colour "0.75", "0.95", "0.85"\n'\
                        '.Wireframe "False"\n'\
                        '.Transparency "0"\n'\
                        '.Create\n'\
                        'End With'

    cst_project.modeler.add_to_history("define material:FR-4 (loss free)", par_change_mesh, timeout=None)    
#define Parameter List
def CstParameterList(cst_project,widthsub,lengthsub):
    par_change = 'Sub Main () \n StoreParameter("widthsub", '+str(widthsub)+')'\
                    '\n StoreParameter("lengthsub", '+str(lengthsub)+')'\
                    '\n StoreParameter("hsub", '+str(1.6)+')'\
                    '\n StoreParameter("meta_thick", '+str(0.035)+')'\
                    '\n StoreParameter("Epsilon_r", '+str(4.3)+')'\
                    '\n StoreParameter("Length", '+str(5)+')' +\
                    '\n StoreParameter("InnerDiameter", '+str(1)+')'\
                    '\n StoreParameter("OuterDiameter", '+str(5.635)+')'\
                    '\n StoreParameter("OuterConductorThickness", '+str(0.5635)+')'\
                    '\nRebuildOnParametricChange (bfullRebuild, bShowErrorMsgBox)'\
                    '\nEnd Sub' 
    cst_project.schematic.execute_vba_code(par_change, timeout=None)   
#define brick Substrate
def CstSubstrate(cst_project):
    par_change_mesh = 'With Brick\n'\
                        '\t.Reset\n'\
                        '\t.Name "Substrate"\n'\
                        '\t.Component "component1"\n'\
                        '\t.Material "FR-4 (loss free)"\n'\
                        '\t.Xrange "-widthsub/2", "widthsub/2"\n'\
                        '\t.Yrange "-lengthsub/2", "lengthsub/2"\n'\
                        '\t.Zrange "-hsub", "0"\n'\
                        '\t.Create\n'\
                        'End With'

    cst_project.modeler.add_to_history("define brick: component1:Substrate", par_change_mesh, timeout=None)        
#define brick Ground
def CstGround(cst_project):
    par_change_mesh = 'With Brick\n'\
                        '\t.Reset\n'\
                        '\t.Name "Ground"\n'\
                        '\t.Component "component1"\n'\
                        '\t.Material "Copper (annealed)"\n'\
                        '\t.Xrange "-widthsub/2", "widthsub/2"\n'\
                        '\t.Yrange "-lengthsub/2", "lengthsub/2"\n'\
                        '\t.Zrange "-hsub", "-hsub-meta_thick"\n'\
                        '\t.Create\n'\
                        'End With'

    cst_project.modeler.add_to_history("define brick: component1:Ground", par_change_mesh, timeout=None)
#define brick Coax
def CstCoax(cst_project):
    par_change_mesh ='With Cylinder\n'\
                        '\t.Reset\n'\
                        '\t.Name "InnerConductor"\n'\
                        '\t.Component "Coax"\n'\
                        '\t.Material "Copper (annealed)"\n'\
                        '\t.OuterRadius "InnerDiameter/2"\n'\
                        '\t.InnerRadius "0"\n'\
                        '\t.Axis "z"\n'\
                        '\t.Zrange "-Length", "meta_thick"\n'\
                        '\t.Xcenter "0"\n'\
                        '\t.Ycenter "0"\n'\
                        '\t.Segments "0"\n'\
                        '\t.Create\n'\
                        'End With\n'\
                        '\'----------------------------------------------------------------------------\n'\
                        'With Cylinder\n'\
                        '\t.Reset\n'\
                        '\t.Name "Dielectric"\n'\
                        '\t.Component "Coax"\n'\
                        '\t.Material "FR-4 (loss free)"\n'\
                        '\t.OuterRadius "OuterDiameter/2"\n'\
                        '\t.InnerRadius "InnerDiameter/2"\n'\
                        '\t.Axis "z"\n'\
                        '\t.Zrange "-Length", "0"\n'\
                        '\t.Xcenter "0"\n'\
                        '\t.Ycenter "0"\n'\
                        '\t.Segments "0"\n'\
                        '\t.Create\n'\
                        'End With\n'\
                        '\'----------------------------------------------------------------------------\n'\
                        'With Cylinder\n'\
                        '\t.Reset\n'\
                        '\t.Name "OuterConductor"\n'\
                        '\t.Component "Coax"\n'\
                        '\t.Material "Copper (annealed)"\n'\
                        '\t.OuterRadius "OuterDiameter/2+OuterConductorThickness"\n'\
                        '\t.InnerRadius "OuterDiameter/2"\n'\
                        '\t.Axis "z"\n'\
                        '\t.Zrange "-Length", "-hsub"\n'\
                        '\t.Xcenter "0"\n'\
                        '\t.Ycenter "0"\n'\
                        '\t.Segments "0"\n'\
                        '\t.Create\n'\
                        'End With'
    cst_project.modeler.add_to_history("define brick: Coax:Coax", par_change_mesh, timeout=None)  

def get_result_antenna(self):
    project = cst.results.ProjectFile(r"C:\DATA\Master\Antenna\Anten_pixel.cst",allow_interactive=True)
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



mycst = cst.interface.DesignEnvironment(mode=cst.interface.DesignEnvironment.StartMode.ExistingOrNew)
myproject = mycst.new_mws()
CstMeshInitiator(myproject)
frequency_min=1
frequency_max=10
CstDefineUnits(myproject)
CstDefineFrequencyRange(myproject,frequency_min,frequency_max)
CstDrawBox(myproject)
CstMeshInitiator(myproject)
CstFD_TETsetting(myproject)
# CstDimsDefineg(myproject)
CstSolverType(myproject)
CstMaterialeFR4(myproject)
CstMaterialeCopper(myproject)
widthsub=50
lengthsub=50
CstParameterList(myproject,widthsub,lengthsub)
CstSubstrate(myproject)
CstCoax(myproject)



# myproject.modeler.run_solver()    
# myproject,allow_interactive=True
# x=myproject.filename()    
# print(x)
# project = cst.results.ProjectFile(x,allow_interactive=True)

# results = project.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
# mycst = cst.interface.DesignEnvironment()
# myproject = cst.interface.DesignEnvironment.new_mws(mycst)

# CstMeshInitiator(myproject)
# frequency_min=1
# frequency_max=10
# CstDefineUnits(myproject)
# CstDefineFrequencyRange(myproject,frequency_min,frequency_max)
# CstDrawBox(myproject)
# CstMeshInitiator(myproject)
# CstFD_TETsetting(myproject)
# CstDimsDefineg(myproject)
# CstSolverType(myproject)



# mycst = cst.interface.DesignEnvironment(mode=cst.interface.DesignEnvironment.StartMode.ExistingOrNew)
# # myproject = mycst.open_project(r'E:\Master\Antenna\Anten_AThang.cst')
# # cst_file = r"E:\Master\Python_code\ANTENNA\Anten_pixel.cst"
# # prj = mycst2.open_project(cst_file)
# mycst1 = cst.interface.DesignEnvironment.open_project(mycst,r'E:\Master\Antenna\Anten_pixel.cst')
# # par_change = 'Sub Main () \nStoreParameter("wg_h", ’+str(0.3)+’)\nStoreParameter("groundplane_length",’+str(12)+’)\nRebuildOnParametricChange (bfullRebuild, bShowErrorMsgBox)\nEnd Sub'
# pixel_size=2
# delta_pixel=1
# x=0
# y=2
# arr2 = np.random.randint (2, size = (5,5))

# par_change1 = 'With Extrude\n'\
#                 '\t.Reset\n'\
#                 '\t.Name \"Pixel_Ant_'+str(x)+'_'+str(y)+'\"\n'\
#                 '\t.Component \"Antenna\"\n'\
#                 '\t.Material \"Copper (annealed)\"\n'\
#                 '\t.Mode \"Pointlist\"\n'\
#                 '\t.Height \"meta_thick\"\n'\
#                 '\t.Twist \"0.0\"\n'\
#                 '\t.Taper \"0.0\"\n'\
#                 '\t.Origin \"0.0\", \"0.0\", \"0.0\"\n'\
#                 '\t.Uvector \"1.0\", \"0.0\", \"0.0\"\n'\
#                 '\t.Vvector \"0.0\", \"1.0\", \"0.0\"\n'\
#                 '\t.Point \"'+str(x*2*pixel_size+(y%2)*pixel_size-pixel_size)+'\", \"'+str(y*(3*pixel_size/2)+pixel_size/2)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size-pixel_size/2)+'\", \"'+str(y*(3*pixel_size/2)+pixel_size/2)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size-pixel_size/2)+'\", \"'+str(y*(3*pixel_size/2)+pixel_size)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size+pixel_size/2)+'\", \"'+str(y*(3*pixel_size/2)+pixel_size)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size+pixel_size/2)+'\", \"'+str(y*(3*pixel_size/2)+pixel_size/2)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size+pixel_size)+'\", \"'+str(y*(3*pixel_size/2)+pixel_size/2)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size+pixel_size)+'\", \"'+str(y*(3*pixel_size/2)-pixel_size/2)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size+pixel_size/2)+'\", \"'+str(y*(3*pixel_size/2)-pixel_size/2)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size+pixel_size/2)+'\", \"'+str(y*(3*pixel_size/2)-pixel_size)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size-pixel_size/2)+'\", \"'+str(y*(3*pixel_size/2)-pixel_size)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size-pixel_size/2)+'\", \"'+str(y*(3*pixel_size/2)-pixel_size/2)+'\"\n'\
#                 '\t.LineTo \"'+str(x*2*pixel_size+(y%2)*pixel_size-pixel_size)+'\", \"'+str(y*(3*pixel_size/2)-pixel_size/2)+'\"\n'\
#                 '\t.Create\n'\
#                 'End With'

# mycst1.modeler.add_to_history( "Pixel_Ant_"+str(x)+"_"+str(y), par_change1 , timeout = None )
# mycst1.schematic.execute_vba_code(par_change, timeout=None)
# mycst1.modeler.run_solver()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
