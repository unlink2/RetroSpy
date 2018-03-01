import keyboard
from ControllerReader import ControllerReader
from axel import Event
from ControllerState import ControllerStateBuilder


class KeyboardReader(ControllerReader):
    def __init__(self, packet_parser):
        self.controllerstate = Event()
        self.controllerdisconnected = Event()

        self.packet_parser = packet_parser

        self.monitor = KeyboardMonitor()
        self.monitor.packet_recv += self.packetrecv
        self.monitor.controllerdisconnected += self.finish

    def finish(self):
        self.monitor.finish()

    def update(self, data=None):
        pass

    def packetrecv(self, packet):
        state = self.packet_parser(self, packet)
        self.controllerstate(self, state)


class KeyboardMonitor:
    def __init__(self):
        self.packet_recv = Event()
        self.controllerdisconnected = Event()
        # all keyevents are hooked here
        keyboard.on_press(callback=self.on_down)
        keyboard.on_release(callback=self.on_release)

        self.buffer = {}

    # data always is a dict of type, name, val
    def on_down(self, data):
        if data is None:
            return
        self.buffer[data.name] = {'type': 'button', 'name': data.name, 'val': True}
        self.packet_recv(self.buffer)

    def on_release(self, data):
        if data is None:
            return
        self.buffer[data.name] = {'type': 'button', 'name': data.name, 'val': False}
        self.packet_recv(self.buffer)

    def finish(self):
        keyboard.unhook_all()


class KeyboardParser:
    @staticmethod
    def readFromPacket(sender, packet):
        state = ControllerStateBuilder()
        for key in packet:
            p = packet[key]
            if p['type'] == 'button':
                state.setButton(p['name'], p['val'])

        return state.build()
