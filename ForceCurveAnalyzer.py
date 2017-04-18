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
import modules.LoadData
import modules.DataProcess

# Define functions for the GUI menu.


def StartDataAnaysis():
    global PlotForceCurves
    PlotForceCurves = PFC.get()
    global SaveForceCurves
    SaveForceCurves = SFC.get()
    modules.DataProcess.DataProcess(
        PathToFile, PlotForceCurves, SaveForceCurves)


def SelectData():
    global PathToFile
    PathToFile = modules.LoadData.LoadData()

# Define the function for a GUI window to set the preferred options


def SummonGUI():
    master = Tk()
    master.title("Force Curve Analyzer")

    Label(master, text="Force Curve analyzer", font=(
        "Helvetica", 16)).grid(row=0, sticky=W, columnspan=2)
    Button(master, text='Load Data Files', command=SelectData).grid(
        row=1, pady=4, columnspan=2)
    Label(master, text="Please select your options:").grid(row=2, columnspan=2)
    global PFC
    PFC = IntVar()
    Checkbutton(master, text="Show all forcecurves",
                variable=PFC).grid(row=3, columnspan=2)
    global SFC
    SFC = IntVar()
    Checkbutton(master, text="Save all forcecurves",
                variable=SFC).grid(row=4, columnspan=2)
    Button(master, text='Execute', command=StartDataAnaysis).grid(
        row=5, column=0, pady=4)
    Button(master, text='Exit', command=master.destroy).grid(
        row=5, column=1, pady=4)
    master.attributes('-topmost', True)
    master.lift()
    mainloop()

# Summon the GUI if this function is called specifically
if __name__ == "__main__":
    SummonGUI()
