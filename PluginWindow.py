import tkinter as tk
from util import plugins


class PluginWindow():
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.title('Plugins')

        plabel = tk.Label(self.window, text='Loaded Plugins:')
        plabel.pack()

        self.pluginlist = tk.Listbox(self.window)

        for i in range(0, len(plugins.plugins)):
            self.pluginlist.insert(i, plugins.plugins[i].name)

        self.pluginlist.pack(side=tk.LEFT)

