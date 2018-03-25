import tkinter as tk
from util import plugins
import tkinter as tk
import string
import util


class PluginWindow():
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.title('Plugins')

        self.pluginmenu_var = tk.StringVar()
        self.add_plugin_list()

        self.reload_p_button = tk.Button(self.window, text='Reload All Plugins', command=self.reload_click)
        self.reload_p_button.pack()

        self.pluginvar = tk.StringVar(root, 'No Plugin Selected')

        pinfo = tk.Label(self.window, textvariable=self.pluginvar)
        pinfo.pack()

        self.enabled_var = tk.IntVar()
        self.enable_checkbox = tk.Checkbutton(self.window, text='Enabled',
                variable=self.enabled_var, command=self.enabled_click)
        self.enable_checkbox.pack()

        self.p_settings_button = tk.Button(self.window, text='Show Plugin Settings', command=self.show_p_settings)
        self.p_settings_button.pack()

        #self.pluginlist = tk.Listbox(self.window)

        #for i in range(0, len(plugins.plugins)):
            #self.pluginlist.insert(i, plugins.plugins[i].name)

        #self.pluginlist.pack(side=tk.LEFT)
        self.update()


    def add_plugin_list(self):
        plabel = tk.Label(self.window, text='Loaded Plugins:')
        plabel.pack()


        self.portmenu = tk.OptionMenu(self.window, self.pluginmenu_var, [], '')
        self.portmenu.pack(side=tk.TOP, pady=10)
        self.pop_plugin_list()

    def pop_plugin_list(self):
        menu = self.portmenu.children['menu']
        menu.delete(0, 'end')

        for p in plugins.all_plugins:
            self.pluginmenu_var.set(p.name)
            menu.add_command(label=p.name, command=lambda v=p.name: self.pluginmenu_var.set(v))

    def enabled_click(self):
        currplugin = self.pluginmenu_var.get()
        if self.enabled_var.get() == 1:
            util.settings.set_bool('enabled', True, section=currplugin)
        else:
            util.settings.set_bool('enabled', False, section=currplugin)

    def reload_click(self):
        util.plugins.load_all()
        self.pop_plugin_list()

        # add root to all plugins
        for p in util.plugins.all_plugins:
            p.on_view(tk_root=self.root)


    def show_p_settings(self):
        for p in util.plugins.all_plugins:
            if p.name == self.pluginmenu_var.get():
                p.on_menu_pressed()

    def update(self):
        # if len(self.pluginlist.curselection()) > 0:
        curplugin = self.pluginmenu_var.get()
        # find plugin
        for p in plugins.all_plugins:
            if p.name == curplugin:
                self.pluginvar.set('Author: ' + p.author + '\nVersion: ' + p.version)
                if not util.settings.does_key_exist('enabled', section=p.name) or \
                        util.settings.get_bool('enabled', section=p.name):
                            self.enabled_var.set(1)
                else:
                    self.enabled_var.set(0)

        self.window.after(100, self.update)
