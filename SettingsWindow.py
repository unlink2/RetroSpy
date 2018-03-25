import tkinter as tk
from util import plugins
import tkinter as tk
import string
import util


class SettingsWindow():
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.title('Settings')

        self.update_var = tk.IntVar()
        self.update_checkbox = tk.Checkbutton(self.window, text='Check for update',
                variable=self.update_var, command=self.update_click)
        self.update_checkbox.pack()

        if util.settings.get_bool('check_updates'):
            self.update_var.set(1)
        else:
            self.update_var.set(0)

        self.update()

    def update_click(self):
        if self.update_var.get() == 1:
            util.settings.set_bool('check_updates', True)
        else:
            util.settings.set_bool('check_updates', False)

    def update(self):
        self.window.after(100, self.update)
