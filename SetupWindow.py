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
from inputs import devices
import util
import webbrowser
from PluginWindow import PluginWindow
from tkinter import filedialog
from CustomWidgets import PopupListbox
from SettingsWindow import SettingsWindow
import sys


class SetupWindow:
    def __init__(self):
        self.root = tk.Tk()

        self.portmenu = None
        self.portmenuvar = tk.StringVar('')
        self.portmenuvar_display = tk.StringVar('')
        self.backgroundlist = None
        self.skinlist = None
        self.lastbgselection = -1
        self.selectedskin = None

        self.root.minsize(width=370, height=280)
        self.root.maxsize(width=370, height=280)
        self.root.title('Setup')

        # right click menu
        # self.right_menu = PopupListbox(self.root, selectmode='multiple')
        # self.right_menu.pack()

        if not os.path.isdir('skins'):
            tk.messagebox.showerror("Error", "Could not find skins folder!")
            return
        self.skins = Skin.loadAllSkinsFromParentFolder(util.settings.get_str('skin_path'))

        if len(self.skins.pare_errors) > 0:
            self.showSkinParseError(self.skins.pare_errors)

        if len(util.plugins.errors) > 0:
            self.showPluginError(util.plugins.errors)

        # add root to all plugins
        for p in util.plugins.all_plugins:
            p.on_view(tk_root=self.root)

        # grid layout
        self.frame = tk.Frame()
        self.frame.pack()
        self.frame.columnconfigure(4) # add 4 columns
        self.frame.rowconfigure(4) # add 4 rows

        device_label = tk.Label(self.frame, text='Input Devices:')
        device_label.grid(row=0, column=0)

        background_label = tk.Label(self.frame, text='Backgrounds:')
        background_label.grid(row=0, column=3)

        self.addPortList()
        self.addSkinList()
        self.addBackgroundList()

        gob = tk.Button(self.frame, text='go!', command=self.goPressed)
        gob.grid(row=4, column=3, padx=5)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label='Preview', command=self.editPressed)
        self.filemenu.add_command(label='Settings', command=self.settings_pressed, accelerator='Ctrl+S')
        self.filemenu.add_command(label='Plugins', command=self.plugins_pressed, accelerator='Ctrl+P')
        self.filemenu.add_command(label='About', command=self.aboutPressed)

        self.pluginsmenu = tk.Menu(self.menubar)
        for p in util.plugins.all_plugins:
            if not p.hide_menu:
                self.pluginsmenu.add_command(label=p.name, command=p.on_menu_pressed)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label='Plugins', menu=self.pluginsmenu)

        # keyboard shortcuts
        self.root.bind_all('<Control-p>', self.plugins_pressed)
        self.root.bind_all('<Control-s>', self.settings_pressed)

        self.root.after(100, self.update)
        self.root.after(1000, self.portListUpdater)
        self.check_update()

        self.root.mainloop()

    def check_update(self):
        if not util.settings.get_bool('check_updates'):
            return
        util.updater.check_update()
        if util.updater.update_available:
            result = tk.messagebox.askquestion('Update available', 'Would you like to download it?')
            if result == 'yes':
                webbrowser.open(util.updater.update_url)

    def settings_pressed(self, *args, **kwargs):
        SettingsWindow(self.root)

    def goPressed(self):
        # make sure a selection has been made!
        if self.selectedskin is None:
            tk.messagebox.showwarning('You are not prepared!', 'You need to select an input device first!')
            return

        if len(self.backgroundlist.curselection()) <= 0:
            tk.messagebox.showwarning('You are not prepared!', 'You need to select a background first!')
            return

        curbg = self.backgroundlist.get(self.backgroundlist.curselection()[0])

        if self.selectedskin.type_str == 'keyboard' or self.selectedskin.type_str == 'keyboard_legacy':
            # check for root
            if not isUserRoot():
                tk.messagebox.showwarning("Root Required", "You must be root to use the keybard viewer!")
                return

        # set settings
        util.settings.set_str('last_sel', self.portmenuvar.get())
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

    def plugins_pressed(self, *args, **kwargs):
        PluginWindow(self.root)

    def addBackgroundList(self):
        self.backgroundlist = tk.Listbox(self.frame)

        self.backgroundlist.grid(row=1, column=3, columnspan=1, rowspan=2, padx=1)

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
        self.skinlist = tk.Listbox(self.frame)

        for i in range(0, len(self.skins.skins_loaded)):
            self.skinlist.insert(i, self.skins.skins_loaded[i].name)

        self.skinlist.grid(row=1, column=0, columnspan=1, rowspan=2, padx=1)

    def addPortList(self):
        self.portmenu = tk.OptionMenu(self.frame, self.portmenuvar_display, [], '')
        self.portListUpdater()
        self.portmenu.grid(pady=0, padx=0, row=4, column=0, columnspan=1, rowspan=1)

    def portListUpdater(self):
        if self.portmenu is None:
            return

        menu = self.portmenu.children['menu']
        menu.delete(0, 'end')

        last_sel_present = False
        last_sel = util.settings.get_str('last_sel')

        if last_sel is None:
            last_sel = ''

        self.comports = list_ports.comports()
        for p in self.comports:
            if p.device == last_sel:
                last_sel_present = True
            menu.add_command(label=p.device, command=lambda v=p.device: self.portmenuvar.set(v))

        for d in devices.keyboards:
            if d._device_path == last_sel:
                last_sel_present = True
            menu.add_command(label=d._device_path, command=lambda v=d._device_path: self.portmenuvar.set(v))

        #for d in devices.mice:
        #    menu.add_command(label=d._device_path, command=lambda v=d._device_path: self.portmenuvar.set(v))

        for d in devices.gamepads:
            if d._device_path == last_sel:
                last_sel_present = True
            menu.add_command(label=d._device_path, command=lambda v=d._device_path: self.portmenuvar.set(v))

        # add legacy keyboard option
        # menu.add_command(label='legacy_keyboard', command=lambda v='legacy_keyboard': self.portmenuvar.set(v))

        if self.portmenuvar.get() == '' and len(self.comports) > 0:
            self.portmenuvar.set(self.comports[0].device)
            if not last_sel == '' and last_sel_present:
                self.portmenuvar.set(last_sel)

        self.root.after(10000, self.portListUpdater)

    def update(self):
        # update port menu var display
        self.portmenuvar_display.set(self.portmenuvar.get()[:12])
        if self.skinlist is not None and \
            len(self.skinlist.curselection()) > 0 and \
                self.skinlist.curselection()[0] != self.lastbgselection:
            self.lastbgselection = self.skinlist.curselection()[0]
            self.updateBackgroundList()

        # update plugins
        for p in util.plugins.plugins:
            p.update()

        self.root.after(100, self.update)

    def showSkinParseError(self, errors):
        errorstr = 'Some skins were unable to be parsed:\n\n'
        for err in errors:
            errorstr = errorstr + str(err) + '\n'

        tk.messagebox.showerror('Error', errorstr)

    def showPluginError(self, errors):
        errorstr = 'Error while loading plugins:\n\n'

        for err in errors:
            errorstr = errorstr + str(err) + '\n'

        tk.messagebox.showerror('Error', errorstr)
