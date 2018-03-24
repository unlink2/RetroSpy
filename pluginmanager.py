import os
import importlib
import imp
import util
import atexit


class PluginManager:
    def __init__(self):
        self.errors = []
        self.plugins_list = [] # list of plugins
        self.load_modules(util.settings.get_str('plugin_path'))
        print('Loaded ', len(self.all_plugins), 'plugins with', len(self.errors), 'errors')
        for e in self.errors:
            print(e)

    def load_modules(self, path):
        # close all exisitng plugins in case of reload
        for p in self.all_plugins:
            p.at_exit()

        self.plugins_list.clear()
        for d in os.listdir(path):
            if d == '.' or d == '..':
                continue
            try:
                mod = load_from_file(os.path.join(path, d))
                if mod is None:
                    continue

                mod.cli_args = util.cli_args
                mod.settings = util.settings
                mod.on_create()
                self.plugins_list.append(mod)
            except Exception as e:
                self.errors.append(e)

    # returns all enabled plugins
    @property
    def plugins(self):
        enabled_list = []
        for p in self.plugins_list:
            if not util.settings.does_key_exist('enabled', section=p.name) or \
                util.settings.get_bool('enabled', section=p.name):
                    enabled_list.append(p)

        return enabled_list

    @property
    def all_plugins(self):
        return self.plugins_list

def load_from_file(filepath):
    class_inst = None
    expected_class = 'Plugin'
    py_mod = None

    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if py_mod is None:
        return None

    if hasattr(py_mod, expected_class):
        class_inst = getattr(py_mod, expected_class)()

    return class_inst


class BasePlugin:
    def __init__(self):
        self.name = ''
        self.author = ''
        self.version = '1.0'
        self.cli_args = None
        self.skin = None
        self.input_tag = ''
        self.comport = ''
        self.tk_root = None
        atexit.register(self.at_exit)
        self.settings = None
        self.hide_menu = False

    def on_create(self):
        pass

    def on_view(self, skin=None, tk_root=None, input_tag='', comport=''):
        self.skin = skin
        self.input_tag = input_tag
        self.comport = comport
        self.tk_root = tk_root

    # called when menu is pressed
    def on_menu_pressed(self):
        pass

    def on_close(self):
        pass

    def at_exit(self):
        pass

    def update(self, input_state=None):
        pass

    def on_action(self, key='', state=False):
        pass
