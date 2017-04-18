def LoadData():
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import filedialog

    # Prepare empty list
    global PathToFile
    PathToFile = []

    # Open the data files using a GUI
    root = tk.Tk()
    root.withdraw()

    tk.messagebox.showinfo(title="Approach data",
                           message="Please select the approach data .txt file")
    PathToFile.append(tk.filedialog.askopenfilename())
    tk.messagebox.showinfo(title="Retract data",
                           message="Please select the retract data .txt file")
    PathToFile.append(tk.filedialog.askopenfilename())

    return PathToFile