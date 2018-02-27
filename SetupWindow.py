# This is the main setup window of NintendoSpyMP
import os
import tkinter as tk
from tkinter import messagebox
import Skin
from serial.tools import list_ports

class SetupWindow:
    def __init__(self):
        self.root = tk.Tk()

        if not os.path.isdir('skins'):
            tk.messagebox.showerror("Error", "Could not find skins folder!")
            return
        self.skins = Skin.loadAllSkinsFromParentFolder('skins')

        for e in self.skins.pare_errors:
            print(e)

        self.createComPortMenu()

        self.root.mainloop()

    def createComPortMenu(self):
        variable = tk.StringVar(self.root)

        ports = list_ports.comports()
        for p in ports:
            variable.set(p) # default value

        w = tk.OptionMenu(self.root, variable, *ports, '')
        w.pack()
