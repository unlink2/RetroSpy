from pluginmanager import BasePlugin


class Plugin(BasePlugin):
    def __init__(self):
        super(BasePlugin, self).__init__()
        self.name = 'sample_plugin'
        self.author = 'unlink'
        self.version = '1.0'
        self.hide_menu = True

    def update(self, input_state=None):
        pass

    def on_action(self, key='', state=False):
        print('Action!', key, state)
        print(self.skin, self.comport, self.input_tag)

    def on_menu_pressed(self):
        print('Menu pressed')

    def on_close(self):
        pass
