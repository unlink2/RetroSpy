from pluginmanager import BasePlugin

class Plugin(BasePlugin):
    def __init__(self):
        self.name = 'sample_plugin'

    def update(self, input_state=None):
        pass

    def on_action(self, key='', state=False):
        print('Action!', key, state)
