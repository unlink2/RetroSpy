from ControllerReader import ControllerReader
from SerialMonitor import SerialMonitor
from axel import Event
from ControllerState import ControllerStateBuilder


class PreviewReader(ControllerReader):
    def __init__(self, packet_parser):
        self.controllerstate = Event()
        self.controllerdisconnected = Event()

        self.packet_parser = packet_parser

        self.monitor = PreviewMonitor()
        self.monitor.packet_recv += self.packetrecv

    def finish(self):
        pass

    def update(self, data=None):
        self.monitor.read(data)

    def packetrecv(self, packet):
        state = self.packet_parser(self, packet)
        self.controllerstate(self, state)


class PreviewMonitor:
    def __init__(self):
        self.packet_recv = Event()

    # data always is a dict of type, name, val
    def read(self, data):
        if data is None:
            return
        self.packet_recv(data)


class PreviewParser:
    @staticmethod
    def readFromPacket(sender, packet):
        state = ControllerStateBuilder()
        for key in packet:
            p = packet[key]
            if p['type'] == 'button':
                state.setButton(p['name'], p['val'])
            elif p['type'] == 'analog':
                state.setAnalog(p['name'], p['val'])

        return state.build()
