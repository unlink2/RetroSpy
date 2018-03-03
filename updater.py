import os
import sys
import util


class Updater:
    def __init__(self):
        self.update_available = False

    def check_update(self):
        pass

    def download(self):
        pass

    def restart(self):
        os.execl(sys.executable, *([sys.executable] + sys.argv))
        sys.exit(0)

    @staticmethod
    def version_str():
        return '{}.{}.{}'.format(util.VERSION_MAJOR, util.VERSION_MINOR, util.VERSION_PATCH)
