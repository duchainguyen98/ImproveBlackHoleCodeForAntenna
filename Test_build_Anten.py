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

#Dim sDefine As String
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

mycst = cst.interface.DesignEnvironment()
mycst2 = cst.interface.DesignEnvironment.new_mws(mycst)

# CstMeshInitiator(mycst2)
frequency_min=1
frequency_max=10
CstDefineUnits(mycst2)
CstDefineFrequencyRange(mycst2,frequency_min,frequency_max)
CstDrawBox(mycst2)
CstMeshInitiator(mycst2)
CstFD_TETsetting(mycst2)
CstDimsDefineg(mycst2)
CstSolverType(mycst2)
# mycst2_mws= mycst2.
# cst_file = r"E:\Master\Python_code\ANTENNA\cst_file.cst"
# prj = mycst2.open_project(cst_file)
# mycst1 = cst.interface.DesignEnvironment.open_project(mycst,r'E:\Master\Antenna\Patch.cst')
# par_change = 'Sub Main () \nStoreParameter("wg_h", ’+str(0.3)+’)\nStoreParameter("groundplane_length",’+str(12)+’)\nRebuildOnParametricChange (bfullRebuild, bShowErrorMsgBox)\nEnd Sub'


# par_change1 = 'With Brick \n.Name "CPW_slot"\n.Component "Antenna"\n .Material "Vacuum"\n.Xrange "1","10"\n.Yrange "1","10"\n.Zrange "0","10"\n.Create\nEnd With'
#
# mycst1.modeler.add_to_history( "AT", par_change1 , timeout = None )
# mycst1.schematic.execute_vba_code(par_change, timeout=None)
# mycst1.modeler.run_solver()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
