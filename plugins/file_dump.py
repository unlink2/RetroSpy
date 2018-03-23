# this plugin dumps all inputs to a specified text file
from pluginmanager import BasePlugin
import os


class Plugin(BasePlugin):
    def __init__(self):
        super(BasePlugin, self).__init__()
        self.name = 'file_dump'
        self.author = 'unlink'
        self.version = '1.0'

    def on_create(self):
        # set up settings that are required
        self.settings.set_defaults({
            self.name: {
                'enable_dumping': 'False',
                'path': ''
            }
        })

        self.dodump = False
        if self.settings.get_bool('enable_dumping', section=self.name):
            path = self.settings.get_str('path', section=self.name)
            if path is not None:
                try:
                    self.f = open(path, 'w')
                    self.dodump = True
                except Exception as e:
                    print(e)
                    self.dodump = False

    def update(self, input_state=None):
        if input_state is not None and self.dodump:
            self.f.write(str(input_state.time) + ': ' + str(input_state.buttons) + '\n' + str(input_state.analogs) + '\n\n')

    def on_action(self, key='', state=False):
        print('Action!', key, state)
        print(self.skin, self.comport, self.input_tag)

    def on_menu_pressed(self):
        print('Menu pressed')

    def on_close(self):
        if self.dodump:
            self.f.close()
