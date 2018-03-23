import time


class ControllerState:
    # buttons is a dict of string, bool
    # analogs is a dict of string, float
    def __init__(self, buttons, analogs):
        self.buttons = buttons
        self.analogs = analogs
        self.time = time.time()


class ControllerStateBuilder:
    def __init__(self):
        self.buttons = {}
        self.analogs = {}

    def setButton(self, name, value):
        self.buttons[name] = value

    def setAnalog(self, name, value):
        self.analogs[name] = value

    def build(self):
        return ControllerState(self.buttons, self.analogs)
