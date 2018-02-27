from ControllerReader import ControllerReader
from SerialMonitor import SerialMonitor
from axel import Event


class SerialControllerReader(ControllerReader):
    def __init__(self, portname, packet_parser):
        self.packet_parser = packet_parser

        self.serial = SerialMonitor(serial_port=portname)
        self.serial.packet_recv += self.serialmonitor_packetrecv
        self.serial.disconnected += self.serialmonitor_disconnected

    def serialmonitor_disconnected(self, data, *args, **kwargs):
        self.finish()
        self.controllerdisconnected(self)

    def serialmonitor_packetrecv(self, packet, *args, **kwargs):
        state = self.packet_parser(packet)
        if state is not None:
            self.controllerstate(self, state)

    def finish(self):
        self.serial.stop()
