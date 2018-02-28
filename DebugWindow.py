# This tk winodw is used to log the state of pins

import time
from InputSource import InputSource
from ControllerState import ControllerState

# This is the experimental mega drive input view window.
# This will move to the normal view window once it is implemented.


class DebugWindow:
    def __init__(self, comport, ui=0.05, device_type = 'nes'):
        self.inputsource = InputSource.makeInputSource(device_type)
        self.inputsource.makeControllerReader(comport=comport)
        self.inputsource.controllerreader.controllerstate += self.on_state

        self.last_state = ControllerState({}, {})

        self.ui = ui
        self.running = True

        while self.running:
            self.update()

    def update(self):
        self.inputsource.controllerreader.update()
        print(self.last_state.buttons)
        print(self.last_state.analogs)
        time.sleep(self.ui)

    def on_state(self, sender, newstate, *args, **kwargs):
        self.last_state = newstate
