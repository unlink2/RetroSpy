import os
import importlib
import imp


class PluginManager:
    def __init__(self):
        self.errors = []
        self.plugins = [] # list of plugins
        self.load_modules('plugins')
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
