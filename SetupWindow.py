# This is the main setup window of NintendoSpyMP
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import Menu
import Skin
from serial.tools import list_ports
from ViewWindow import ViewWindow
from PreviewWindow import PreviewWindow
from AboutWindow import AboutWindow
from util import isUserRoot


class SetupWindow:
    def __init__(self):
        self.root = tk.Tk()

        self.portmenu = None
        self.portmenuvar = tk.StringVar('')
        self.backgroundlist = None
        self.skinlist = None
        self.lastbgselection = -1
        self.selectedskin = None

        self.root.minsize(width=350, height=300)
        self.root.maxsize(width=350, height=300)
        self.root.title('Setup')

        if not os.path.isdir('skins'):
            tk.messagebox.showerror("Error", "Could not find skins folder!")
            return
        self.skins = Skin.loadAllSkinsFromParentFolder('skins')

        if len(self.skins.pare_errors) > 0:
            self.showSkinParseError(self.skins.pare_errors)

        self.addPortList()
        self.addSkinList()
        self.addBackgroundList()

        gob = tk.Button(self.root, text='go!', command=self.goPressed)
        gob.pack(side=tk.BOTTOM)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label='Preview', command=self.editPressed)
        self.filemenu.add_command(label='About', command=self.aboutPressed)

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.root.after(100, self.update)
        self.root.after(1000, self.portListUpdater)

        self.root.mainloop()

    def goPressed(self):
        # make sure a selection has been made!
        if self.selectedskin is None:
            return

        if len(self.backgroundlist.curselection()) <= 0:
            return

        curbg = self.backgroundlist.get(self.backgroundlist.curselection()[0])

        if self.selectedskin.type_str == 'keyboard':
            # check for root
            if not isUserRoot():
                tk.messagebox.showwarning("Root Required", "You must be root to use the keybard viewer!")
                return

        ViewWindow(self.root, self.selectedskin, curbg, self.portmenuvar.get())

    def editPressed(self):
        # make sure a selection has been made!
        if self.selectedskin is None:
            return

        if len(self.backgroundlist.curselection()) <= 0:
            return

        curbg = self.backgroundlist.get(self.backgroundlist.curselection()[0])

        PreviewWindow(self.root, self.selectedskin, curbg)

    def aboutPressed(self):
        AboutWindow(self.root)

    def addBackgroundList(self):
        self.backgroundlist = tk.Listbox(self.root)

        self.backgroundlist.pack(side=tk.RIGHT)

    def updateBackgroundList(self):
        if self.backgroundlist is not None:
            self.backgroundlist.delete(0, 'end')

        # get the corerct skin and load all backgrounds into the list
        selectedskinname = self.skinlist.get(self.lastbgselection)
        selectedskin = None
        for skin in self.skins.skins_loaded:
            if skin.name == selectedskinname:
                selectedskin = skin
                break

        self.selectedskin = selectedskin

        if selectedskin is None:
            return

        for i in range(0, len(selectedskin.backgrounds)):
            self.backgroundlist.insert(i, selectedskin.backgrounds[i].name)

    def addSkinList(self):
        self.skinlist = tk.Listbox(self.root)

        for i in range(0, len(self.skins.skins_loaded)):
            self.skinlist.insert(i, self.skins.skins_loaded[i].name)

        self.skinlist.pack(side=tk.LEFT)

    def addPortList(self):
        self.portmenu = tk.OptionMenu(self.root, self.portmenuvar, [], '')
        self.portListUpdater()
        self.portmenu.pack(side=tk.TOP, pady=10)

    def portListUpdater(self):
        if self.portmenu is None:
            return

        menu = self.portmenu.children['menu']
        menu.delete(0, 'end')

        self.comports = list_ports.comports()
        for p in self.comports:
            menu.add_command(label=p.device, command=lambda v=p.device: self.portmenuvar.set(v))

        if self.portmenuvar.get() == '' and len(self.comports) > 0:
            self.portmenuvar.set(self.comports[0].device)

        self.root.after(1000, self.portListUpdater)

    def update(self):
        if self.skinlist is not None and \
            len(self.skinlist.curselection()) > 0 and \
                self.skinlist.curselection()[0] != self.lastbgselection:
            self.lastbgselection = self.skinlist.curselection()[0]
            self.updateBackgroundList()

        self.root.after(100, self.update)

    def showSkinParseError(self, errors):
        errorstr = 'Some skins were unable to be parsed:\n\n'
        for err in errors:
            errorstr = errorstr + str(err) + '\n'

        tk.messagebox.showerror('Error', errorstr)
