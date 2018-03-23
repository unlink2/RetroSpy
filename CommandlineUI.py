# This tk winodw is used to log the state of pins

import time
from InputSource import InputSource
from ControllerState import ControllerState
import util

# This is the experimental mega drive input view window.
# This will move to the normal view window once it is implemented.


class CommandlineUI:
    def __init__(self, comport, ui=0.05, device_type='nes'):
        self.inputsource = InputSource.makeInputSource(device_type)
        self.inputsource.makeControllerReader(comport=comport)
        self.inputsource.controllerreader.controllerstate += self.on_state

        self.last_state = ControllerState({}, {})

        self.ui = ui
        self.running = True

        # call plugin's on_view
        for p in util.plugins.plugins:
            p.on_view(comport=comport, input_tag=device_type)

        while self.running:
            self.update()

        for p in util.plugins.plugins:
            p.on_close()

    def update(self):
        self.inputsource.controllerreader.update()
        # update plugins
        for p in util.plugins.plugins:
            p.update(self.last_state)

        print(self.last_state.time)

        print(self.last_state.buttons)

        print(self.last_state.analogs)
        time.sleep(self.ui)

    def on_state(self, sender, newstate, *args, **kwargs):
        self.last_state = newstate
