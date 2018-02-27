from axel import Event


class ControllerReader:
    def __init(self):
        self.controllerstate = Event()
        self.controllerdisconnected = Event()

    def finish(self):
        pass

    def update(self):
        pass
