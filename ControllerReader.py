from axel import Event


class ControllerReader:
    def __init(self):
        self.controllerstate = Event()
        self.controllerdisconnected = Event()
        self.onerror = Event()

    def finish(self):
        pass

    def update(self, data=None):
        pass
