# this plugin dumps all inputs to a specified text file
from pluginmanager import BasePlugin
import os
import tkinter as tk
from tkinter import filedialog

class Plugin(BasePlugin):
    def __init__(self):
        super(BasePlugin, self).__init__()
        self.name = 'file_dump'
        self.author = 'unlink'
        self.version = '1.0'
        self.hide_menu = False

    def on_create(self):
        # set up settings that are required
        self.settings.set_defaults({
            self.name: {
                'enable_dumping': 'False',
                'path': ''
            }
        })

        self.dodump = False
        if self.settings.get_bool('enable_dumping', section=self.name):
            path = self.settings.get_str('path', section=self.name)
            if path is not None:
                try:
                    self.f = open(path, 'w')
                    self.dodump = True
                except Exception as e:
                    print(e)
                    self.dodump = False

    def update(self, input_state=None):
        if input_state is not None and self.dodump:
            self.f.write(str(input_state.time) + ': ' + str(input_state.buttons) + '\n' + str(input_state.analogs) + '\n\n')

    def on_action(self, key='', state=False):
        print('Action!', key, state)
        print(self.skin, self.comport, self.input_tag)

    def on_menu_pressed(self):
        self.window = tk.Toplevel(self.tk_root)
        self.window.title('View')

        self.enable_dump_var = tk.IntVar()
        self.enable_dump = tk.Checkbutton(self.window, text='Enable Dumping', variable=self.enable_dump_var, command=self.enable_click)
        self.enable_dump.pack()

        # set up value according to config
        if self.settings.get_bool('enable_dumping', section=self.name):
            self.enable_dump_var.set(1)
        else:
            self.enable_dump_var.set(0)

        self.setpath_button = tk.Button(self.window, text='Select dump file', command=self.path_sel_click)
        self.setpath_button.pack()

    def path_sel_click(self):
        path = filedialog.asksaveasfilename(initialdir='./', title='select file')
        if path is not None:
            self.settings.set_str('path', path, section=self.name)

    def enable_click(self):
        if self.enable_dump_var.get() == 1:
            self.settings.set_bool('enable_dumping', True, section=self.name)
        else:
            self.settings.set_bool('enable_dumping', False, section=self.name)

    def on_close(self):
        if self.dodump:
            self.f.close()
