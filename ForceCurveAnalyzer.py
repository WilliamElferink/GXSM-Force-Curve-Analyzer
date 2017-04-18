#####################################
#         About this script         #
#####################################

# This script is designed to obtain the raw data from the GXSM images.
# Its original purpose was to be able to easily extract the individual
# force curves from a multiple force curve measurement. As GXSM puts
# approach and retract movements in two different measurements, it requires
# two files to work (the positive x-scan and negative x-scan files).
#
# It utilizes a txt dump of the .nc files output from GXSM.
# You can obtain these txt dump by entering in the Linux Terminal:
# #####################################
# # ncdump filename.nc > filename.txt #
# #####################################
#
# You might have to install the netcdf binaries first by using
# ###################################
# # sudo apt-get install netcdf-bin #
# ###################################
#
# The txt file generated can now be loaded with this Python script.

##############################################################
#                       --- Part 0 ---                       #
#                       Initialization                       #
##############################################################
import os
import tkinter as tk
from tkinter import *
import modules.LoadForceData
import modules.LoadForceCurrentData
import modules.DataProcess

# Define functions for the GUI menu.


def StartDataAnaysis():
    global PlotForceCurves
    PlotForceCurves = PFC.get()
    global SaveForceCurves
    SaveForceCurves = SFC.get()
    modules.DataProcess.DataProcess(
        PathToFile, PlotForceCurves, SaveForceCurves)


def SelectForceData():
    global PathToFile
    PathToFile = modules.LoadForceData.LoadData()


def SelectForceCurrentData():
    global PathToFile
    PathToFile = modules.LoadForceCurrentData.LoadData()

# Define the function for a GUI window to set the preferred options


def SummonGUI():
    root = Tk()
    root.title("Force Curve Analyzer")

    Label(root, text="Force Curve analyzer", font=(
        "Helvetica", 16)).grid(row=0, sticky=W, columnspan=2)
    Button(root, text='Load Force Curve Files',
           command=SelectForceData).grid(
        row=1, pady=4, columnspan=2)
    Button(root, text='Load Force Curve + Current Files',
           command=SelectForceCurrentData).grid(
        row=2, pady=4, columnspan=2)
    Label(root, text="Please select your options:").grid(row=3, columnspan=2)
    global PFC
    PFC = IntVar()
    Checkbutton(root, text="Show all forcecurves",
                variable=PFC).grid(row=4, columnspan=2)
    global SFC
    SFC = IntVar()
    Checkbutton(root, text="Save all forcecurves",
                variable=SFC).grid(row=5, columnspan=2)
    Button(root, text='Execute', command=StartDataAnaysis).grid(
        row=7, column=0, pady=4)
    Button(root, text='Exit', command=root.destroy).grid(
        row=7, column=1, pady=4)
    root.attributes('-topmost', True)
    root.lift()
    mainloop()

# Summon the GUI if this function is called specifically
if __name__ == "__main__":
    SummonGUI()
