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

    tk.messagebox.showinfo(title="Force curve approach data",
                           message="Please select the force curve approach data .txt file")
    PathToFile.append(tk.filedialog.askopenfilename())
    tk.messagebox.showinfo(title="Force curve retract data",
                           message="Please select the force curve retract data .txt file")
    PathToFile.append(tk.filedialog.askopenfilename())
    tk.messagebox.showinfo(title="Tunnelling current approach data",
                           message="Please select the tunnelling current approach data .txt file")
    PathToFile.append(tk.filedialog.askopenfilename())
    tk.messagebox.showinfo(title="Tunnelling current retract data",
                           message="Please select the tunnelling current retract data .txt file")
    PathToFile.append(tk.filedialog.askopenfilename())

    return PathToFile
