import tkinter as tk
from util import plugins
import tkinter as tk
import string


class PluginWindow():
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.title('Plugins')

        self.pluginvar = tk.StringVar(root, 'No Plugin Selected')

        pinfo = tk.Label(self.window, textvariable=self.pluginvar)
        pinfo.pack()

        plabel = tk.Label(self.window, text='Loaded Plugins:')
        plabel.pack()

        self.pluginlist = tk.Listbox(self.window)

        for i in range(0, len(plugins.plugins)):
            self.pluginlist.insert(i, plugins.plugins[i].name)

        self.pluginlist.pack(side=tk.LEFT)
        self.update()

    def update(self):
        if len(self.pluginlist.curselection()) > 0:
            curplugin = self.pluginlist.get(self.pluginlist.curselection()[0])
            # find plugin
            for p in plugins.plugins:
                if p.name == curplugin:
                    self.pluginvar.set('Author: ' + p.author + '\nVersion: ' + p.version)

        self.window.after(100, self.update)
