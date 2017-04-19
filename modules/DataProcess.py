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
    DataSetConvert = []
    VResponse = []

    ##############################################################
    #                       --- Part 1 ---                       #
    #      Reformatting the .txt data to Python usable data      #
    ##############################################################

    # Load datafiles (.txt) into Python
    for i in range(0, len(PathToFile)):
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
    # Also look up unit type and its conversion rate
    for x in File[0]:
        for y in x:
            if "opt_xpiezo_av =" in y:
                PiezoXAv = float(
                    y.replace("opt_xpiezo_av = ", "").replace(";", ""))
            elif "opt_zpiezo_av =" in y:
                PiezoZAv = float(
                    y.replace("opt_zpiezo_av = ", "").replace(";", ""))
            elif "dz =" in y:
                VResponse.append(float(
                    y.replace("dz = ", "").replace(";", "")))
                VResponse.append(VResponse[0])
            elif "FloatField:unit = " in y:
                UnitType = str(y.replace(
                    "FloatField:unit = \"", "").replace("\" ;", ""))
            elif "sranger_mk2_hwi_XSM_Inst_VZ = " in y:
                GainZ = float(
                    y.replace("sranger_mk2_hwi_XSM_Inst_VZ = ", "").replace(
                        ";", ""))
    if (len(PathToFile) == 4):
        for x in File[2]:
            for y in x:
                if "dz =" in y:
                    VResponse.append(float(
                        y.replace("dz = ", "").replace(";", "")))
                    VResponse.append(VResponse[2])

    # Convert the X-movement to Z-movement in nanometers
    for x in XRange:
        ZMovement.append((x / PiezoXAv) * ((PiezoZAv * GainZ) / 10))

    # Convert deflection data from raw to the requested unit.
    temp = []
    for i in range(0, len(PathToFile)):
        for x in DataSet[i]:
            for y in x:
                temp.append(y * VResponse[i])
            row.append(temp)
            temp = []
        DataSetConvert.append(row)
        row = []

    ##############################################################
    #                       --- Part 3 ---                       #
    #                    Imaging the results                     #
    ##############################################################
    if UnitType == "Hz":
        YAxisLabel = "Frequency shift (Hz)"
    elif UnitType == "V":
        YAxisLabel = "Voltage (V)"
    # Set preferred color codes here if you want different ones
    # Ordered from line 1 to 4. Current settings are Tableau 20 colours
    LineColor = [(31, 119, 180), (174, 199, 232),
                 (255, 127, 14), (255, 187, 120)]

    # Scale colours to the matplotlib format.
    for i in range(len(LineColor)):
        r, g, b = LineColor[i]
        LineColor[i] = (r / 255., g / 255., b / 255.)

    # Set linewidth for each line, ordered 1 to 4.
    DataLineWidth = [2.0, 1.0, 2.0, 1.0]

    # Start plotting and saving of force curves
    if (PlotForceCurves == 1 or SaveForceCurves == 1):
        for i in range(0, DimY[0]):
            if len(PathToFile) == 2:
                fig = plt.figure(i, figsize=(16, 12))
                plt.plot(
                    ZMovement,
                    DataSetConvert[0][i],
                    color=LineColor[0],
                    linewidth=DataLineWidth[0])
                plt.plot(
                    ZMovement,
                    list(reversed(DataSetConvert[1][i])),
                    color=LineColor[1],
                    linewidth=DataLineWidth[1])
                plt.xlabel("Movement in Z-piezo (nm)")
                plt.ylabel(YAxisLabel)
                plt.legend(["Approach force curve",
                            "Retract force curve"],
                           loc='best')
                plt.title("Measurement #%i" % (i + 1))
                if SaveForceCurves == 1:
                    # Creating a new folder for storing images.
                    directory = os.path.split(PathToFile[0])[0]
                    filename = os.path.split(PathToFile[0])[1]
                    newdir = filename.replace(".txt", " Images/")
                    if not os.path.exists(directory + '/' + newdir):
                        os.makedirs(directory + '/' + newdir)
                    plt.savefig(directory + '/' + newdir +
                                'Measurement %i.png' % (i + 1))
            if len(PathToFile) == 4:
                fig = plt.figure(i, figsize=(16, 12))
                ax1 = fig.add_subplot(111)
                l1, = ax1.plot(
                    ZMovement,
                    DataSetConvert[0][i],
                    color=LineColor[0],
                    linewidth=DataLineWidth[0])
                l2, = ax1.plot(
                    ZMovement,
                    list(reversed(DataSetConvert[1][i])),
                    color=LineColor[1],
                    linewidth=DataLineWidth[1])
                ax1.set_xlabel("Movement in Z-piezo (nm)")
                ax1.set_ylabel(YAxisLabel)
                ax1.tick_params('y')
                ax2 = ax1.twinx()
                l3, = ax2.plot(
                    ZMovement,
                    DataSetConvert[2][i],
                    color=LineColor[2],
                    linewidth=DataLineWidth[2])
                l4, = ax2.plot(
                    ZMovement,
                    list(reversed(DataSetConvert[3][i])),
                    color=LineColor[3],
                    linewidth=DataLineWidth[3])
                ax2.set_ylabel("Tunnelling current (nA)")
                ax2.tick_params('y')
                plt.legend([l1, l2, l3, l4], ["Approach force curve",
                                              "Retract force curve",
                                              "Approach tunnelling current",
                                              "Retract tunnelling current"],
                           loc='best',
                           prop={'size': 12})
                plt.title("Measurement #%i" % (i + 1))

            if SaveForceCurves == 1:
                # Creating a new folder for storing images.
                directory = os.path.split(PathToFile[0])[0]
                filename = os.path.split(PathToFile[0])[1]
                newdir = filename.replace(".txt", " Images/")
                if not os.path.exists(directory + '/' + newdir):
                    os.makedirs(directory + '/' + newdir)
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
