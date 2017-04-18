def DataProcess(PathToFile, PlotForceCurves, SaveForceCurves):
    import os
    import matplotlib.pyplot as plt
    import numpy as np
    import subprocess
    import sys
    import platform

    # All the necessary empty list declarations.
    File = []
    DataStart = []
    DataEnd = []
    DimX = []
    DimY = []
    DataSet = []
    temp = []
    forcecurve = []
    row = []
    XRange = []
    ZMovement = []
    DataSetVolt = []

    ##############################################################
    #                       --- Part 1 ---                       #
    #      Reformatting the .txt data to Python usable data      #
    ##############################################################

    # Load datafiles (.txt) into Python
    for i in range(0, 2):
        with open(PathToFile[i]) as f:
            content = f.readlines()
        # Remove white spaces and find the start of the datafields
        File.append([x.strip().split(",") for x in content])
        DataStart.append(File[i].index(["FloatField ="]) + 1)
        # Finding the end of data is a bit more difficult (might become
        # obsolete)
        for x in File[i]:
            for y in x:
                if (("time =" in y) and not ("reftime" in y) and not ("time = 1 ;" in y)):
                    DataEnd.append(File[i].index(x) - 2)
        # Find dimensions of the measurement
        DimX.append(int(File[i][4][0].replace("dimx = ", "").replace(";", "")))
        DimY.append(int(File[i][5][0].replace("dimy = ", "").replace(";", "")))
        # Build the Dataset from the imported datafile
        # Introduce necessary variables
        n = DataStart[i]
        j = 0
        k = 0
        m = 0
        row = []
        forcecurve = []
        # Fill the empty lists
        while k < DimY[i]:
            # Obtain the numbers from one line of the original data file
            temp = list(float(x.replace(";", ""))
                        for x in list(filter(None, File[i][n + m])))
            m = m + 1
            for x in temp:
                row.append(x)
            # Check if the end of a force curve measurement has been reached.
            # If so: go to the next measurement.
            if len(row) == DimX[i]:
                forcecurve.append(row)
                row = []
                k = k + 1
        # Gather all the forcecurves in one dataset.
        DataSet.append(forcecurve)

    # Obtain the data for the X-direction (used as Z) voltage.
    # Find the starting point of the X-voltage dataset
    for x in File[0]:
        for y in x:
            if ("dimx =" in y) and not (("dimx = %s" % DimX[0]) in y):
                DimXStart = File[0].index(x)
    # Reset the necessary variables
    j = 0
    m = 0
    n = DimXStart
    while j < DimX[0]:
        # Obtain the numbers from one line of the original data file
        temp = list(float(x.replace(";", "").replace("dimx = ", ""))
                    for x in list(filter(None, File[0][n + m])))
        m = m + 1
        for x in temp:
            XRange.append(x)
        # Check if the end of the dataset has been reached.
        # If so: save the X data
        if len(XRange) == DimX[i]:
            j = DimX[0]

    ##############################################################
    #                       --- Part 2 ---                       #
    #                 Convert data to correct units              #
    ##############################################################
    # Look up the voltage to movement response as known by GXSM (X, Y and Z)
    for x in File[0]:
        for y in x:
            if "opt_xpiezo_av =" in y:
                PiezoXAv = float(
                    y.replace("opt_xpiezo_av = ", "").replace(";", ""))
            elif "opt_ypiezo_av =" in y:
                PiezoYAv = float(
                    y.replace("opt_ypiezo_av = ", "").replace(";", ""))
            elif "opt_zpiezo_av =" in y:
                PiezoZAv = float(
                    y.replace("opt_zpiezo_av = ", "").replace(";", ""))

    # Convert the X-movement to Z-movement in Angstrom
    for x in XRange:
        ZMovement.append((x / PiezoXAv) * (PiezoZAv / 10))

    # Convert deflection data from raw to voltages.
    # Obtain conversion ratio
    for x in File[0]:
        for y in x:
            if "dz =" in y:
                VResponse = float(y.replace("dz = ", "").replace(";", ""))
    # Convert the dataset
    temp = []
    for i in range(0, 2):
        for x in DataSet[i]:
            for y in x:
                temp.append(y * VResponse)
            row.append(temp)
            temp = []
        DataSetVolt.append(row)
        row = []

    ##############################################################
    #                       --- Part 3 ---                       #
    #                    Imaging the results                     #
    ##############################################################
    # Creating a new folder for storing images.
    directory = os.path.split(PathToFile[0])[0]
    filename = os.path.split(PathToFile[0])[1]
    newdir = filename.replace(".txt", " Images/")
    if not os.path.exists(directory + '/' + newdir):
        os.makedirs(directory + '/' + newdir)

    # Start plotting and saving of force curves
    if (PlotForceCurves == 1 or SaveForceCurves == 1):
        for i in range(0, DimY[0]):
            fig = plt.figure(i)
            plt.plot(ZMovement, DataSetVolt[0][
                     i], 'b-', ZMovement, list(reversed(DataSetVolt[1][i])), 'r-')
            plt.xlabel("Movement in Z-piezo (nm)")
            plt.ylabel("Photodiode voltage/Force (V)")
            plt.legend(["Approach force curve",
                        "Retract force curve"], loc='best')
            plt.title("Measurement #%i" % (i + 1))
            if SaveForceCurves == 1:
                plt.savefig(directory + '/' + newdir +
                            'Measurement %i.png' % (i + 1))
        if PlotForceCurves == 1:
            plt.show()
        if SaveForceCurves == 1:
            path = directory + '/' + newdir
            def open_file(path):
                if platform.system() == "Windows":
                    os.startfile(path)
                elif platform.system() == "Darwin":
                    subprocess.Popen(["open", path])
                else:
                    subprocess.Popen(["xdg-open", path])
            open_file(path)
