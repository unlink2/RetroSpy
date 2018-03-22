import configparser
import atexit


class Settings:
    def __init__(self, path='./settings.ini'):
        self.cfg = configparser.ConfigParser()
        self.path = path
        self.cfg.read(path)
        self.set_defaults()
        atexit.register(self.at_exit)

    def set_defaults(self):
        for section in Settings.DEFAULT_VALUES:
            if section not in self.cfg:
                self.cfg[section] = {}
            for key in Settings.DEFAULT_VALUES[section].keys():
                if key not in self.cfg[section]:
                    self.cfg[section][key] = str(Settings.DEFAULT_VALUES[section][key])

    def write(self):
        with open(self.path, 'w') as configfile:
            self.cfg.write(configfile)

    def at_exit(self):
        self.write()


Settings.DEFAULT_VALUES = {
        'DEFAULT': {
            'plugin_path': 'plugins',
            'skin_path': 'skins',
        }
}

