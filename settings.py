import configparser
import atexit


class Settings:
    def __init__(self, path='./settings.ini'):
        self.cfg = configparser.ConfigParser()
        self.path = path
        self.cfg.read(path)
        self.set_defaults()
        atexit.register(self.at_exit)

    def set_defaults(self, defaults=None):
        if defaults is None:
            defaults = Settings.DEFAULT_VALUES

        for section in defaults:
            if section not in self.cfg:
                self.cfg[section] = {}
            for key in defaults[section].keys():
                if key not in self.cfg[section]:
                    self.cfg[section][key] = str(defaults[section][key])

    def write(self):
        with open(self.path, 'w') as configfile:
            self.cfg.write(configfile)

    def at_exit(self):
        self.write()

    def does_section_exist(self, section='DEFAULT'):
        if section in self.cfg:
            return True
        return False

    def does_key_exist(self, key, section='DEFAULT'):
        if section in self.cfg:
            if key in self.cfg[section]:
                return True

        return False

    def get_str(self, key, section='DEFAULT'):
        if self.does_key_exist(key, section):
            return self.cfg[section][key]
        return None

    def get_int(self, key, section='DEFAULT'):
        try:
            return int(self.get_str(key, section))
        except TypeError as e:
            return None

    def get_float(self, key, section='DEFAULT'):
        try:
            return float(self.get_str(key, section))
        except TypeError as e:
            return None

    def get_bool(self, key, section='DEFAULT'):
        val = self.get_str(key, section)
        if val is not None:
            return val == 'True'
        return False

    def get_section(self, section='DEFAULT'):
        if self.does_section_exist(section):
            return self.cfg[section]
        return None

    def add_section(self, section='DEFAULT'):
        if not self.does_section_exist(section):
            self.cfg[section] = {}

    def set_str(self, key, val, section='DEFAULT'):
        if self.does_section_exist(section):
            self.cfg[section][key] = val

    def set_int(self, key, val, section='DEFAULT'):
        self.set_str(key, str(val), section)

    def set_float(self, key, val, section='DEFAULT'):
        self.set_str(key, str(val), section)

    def set_bool(self, key, val, section='DEFAULT'):
        self.set_str(key, str(val), section)

    def delete_key(self, key, section='DEFAULT'):
        if self.does_key_exist(key, section):
            del self.cfg[section][key]

    def delete_section(self, section='DEFAULT'):
        if self.does_section_exist(section):
            del self.cfg[section]

Settings.DEFAULT_VALUES = {
        'DEFAULT': {
            'plugin_path': 'plugins',
            'skin_path': 'skins',
        }
}

