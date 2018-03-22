import os
import importlib
import imp
import util
import atexit


class PluginManager:
    def __init__(self):
        self.errors = []
        self.plugins = [] # list of plugins
        self.load_modules(util.settings.cfg['DEFAULT']['plugin_path'])
        print('Loaded ', len(self.plugins), 'plugins with', len(self.errors), 'errors')
        for e in self.errors:
            print(e)

    def load_modules(self, path):
        for d in os.listdir(path):
            if d == '.' or d == '..':
                continue
            try:
                mod = load_from_file(os.path.join(path, d))
                if mod is None:
                    continue

                mod.cli_args = util.cli_args
                self.plugins.append(mod)
            except Exception as e:
                self.errors.append(e)


def load_from_file(filepath):
    class_inst = None
    expected_class = 'Plugin'
    py_mod = None

    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])

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
        self.cli_args = None
        self.skin = None
        self.input_tag = ''
        self.comport = ''
        self.tk_root = None
        atexit.register(self.at_exit)

    def write_setting(self, key, val):
        if self.name not in util.settings.cfg:
            util.settings.cfg[self.name] = {}
        util.settings.cfg[self.name][str(key)] = str(val)

    def read_setting(self, key):
        if self.name not in util.settings.cfg:
            return None

        if key not in util.settings.cfg[self.name]:
            return None

        return util.settings.cfg[self.name][str(key)]

    def on_view(self, skin=None, tk_root=None, input_tag='', comport=''):
        self.skin = skin
        self.input_tag = input_tag
        self.comport = comport
        self.tk_root = tk_root

    def on_close(self):
        pass

    def at_exit(self):
        pass

    def update(self, input_state=None):
        pass

    def on_action(self, key='', state=False):
        pass
