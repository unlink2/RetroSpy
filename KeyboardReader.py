import keyboard
from ControllerReader import ControllerReader
from axel import Event
from ControllerState import ControllerStateBuilder
from inputs import get_key
from inputs import UnpluggedError
from inputs import devices
import util

class KeyboardReader(ControllerReader):
    def __init__(self, comport, packet_parser):
        self.controllerstate = Event()
        self.controllerdisconnected = Event()
        self.onerror = Event()

        self.packet_parser = packet_parser
        self.comport = comport

        self.monitor = KeyboardMonitor(comport)
        self.monitor.packet_recv += self.packetrecv
        self.monitor.controllerdisconnected += self.finish

        self.t = None

    def finish(self):
        self.monitor.finish()

    def update(self, data=None):
        self.monitor.update()

    def packetrecv(self, packet):
        state = self.packet_parser(self, packet)
        self.controllerstate(self, state)


class KeyboardMonitor:
    def __init__(self, comport):
        self.comport = comport
        self.packet_recv = Event()
        self.onerror = Event()
        self.controllerdisconnected = Event()
        # all keyevents are hooked here
        if self.comport == 'keyboard_legacy':
            keyboard.on_press(callback=self.on_down)
            keyboard.on_release(callback=self.on_release)

        self.buffer = {}

    def update(self):
        if self.comport == 'keyboard_legacy':
            return
        try:
            kb_event = None
            for d in devices.keyboards:
                if d._device_path == self.comport:
                    kb_event = d.read()

            if kb_event is None:
                kb_event = get_key()

            for e in kb_event:
                val = False
                if e.state > 0:
                    val = True
                if e.ev_type == 'Key':
                    self.on_key_data({'type': 'button', 'name': e.code, 'val': val})

            #mouse_event = get_mouse()
            #for e in mouse_event:
            #    print(e.ev_type, e.code, e.state)

            #controller_event = get_gamepad()

            #for e in controller_event:
            #    print(e.ev_type, e.code, e.state)
        except UnpluggedError as e:
            util.logger.error(str(e))

    def on_key_data(self, data):
        if data is None:
            return
        self.buffer[data['name']] = {'type': data['type'], 'name': data['name'], 'val': data['val']}
        self.packet_recv(self.buffer)

    # deprecated
    # data always is a dict of type, name, val
    def on_down(self, data):
        if data is None:
            return
        self.buffer[data.name] = {'type': 'button', 'name': data.name, 'val': True}
        self.packet_recv(self.buffer)

    # deprecated
    def on_release(self, data):
        if data is None:
            return
        self.buffer[data.name] = {'type': 'button', 'name': data.name, 'val': False}
        self.packet_recv(self.buffer)

    def finish(self):
        if self.comport == 'keyboard_legacy':
            keyboard.unhook_all()


class KeyboardParser:
    @staticmethod
    def readFromPacket(sender, packet):
        state = ControllerStateBuilder()
        for key in packet:
            p = packet[key]
            # check for special cases
            if key == 'shift' or key == 'ctrl' or key == 'windows':
                if p['type'] == 'button':
                    state.setButton('left ' + p['name'], p['val'])
                    state.setButton('right ' + p['name'], p['val'])

            if p['type'] == 'button':
                state.setButton(p['name'], p['val'])

        return state.build()
