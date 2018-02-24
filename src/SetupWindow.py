# This is the main setup window of NintendoSpyMP

import tkinter as tk
import Skin
from serial.tools import list_ports

class SetupWindow:
    def __init__(self):
        self.skins = Skin.loadAllSkinsFromParentFolder('skins')

        for e in self.skins.pare_errors:
            print(e)

        self.root = tk.Tk()

        self.createComPortMenu()

        self.root.mainloop()

    def createComPortMenu(self):
        variable = tk.StringVar(self.root)

        ports = list_ports.comports()
        for p in ports:
            variable.set(p) # default value

        w = tk.OptionMenu(self.root, variable, *ports)
        w.pack()
