from ControllerReader import ControllerReader
from axel import Event
from ControllerState import ControllerStateBuilder
from inputs import get_key
from inputs import get_gamepad
from inputs import get_mouse
from inputs import UnpluggedError
from inputs import devices
from inputs import UnknownEventCode

class GenericControllerReader(ControllerReader):
    def __init__(self, comport, packet_parser):
        self.controllerstate = Event()
        self.controllerdisconnected = Event()

        self.packet_parser = packet_parser
        self.comport = comport

        self.monitor = GenericControllerMonitor(comport)
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


class GenericControllerMonitor:
    def __init__(self, comport):
        self.comport = comport
        self.packet_recv = Event()
        self.controllerdisconnected = Event()

        self.buffer = {}

    def update(self):
        try:
            kb_event = None
            for d in devices.gamepads:
                if d._device_path == self.comport:
                    kb_event = d.read()

            if kb_event is None:
                kb_event = get_gamepad()

            for e in kb_event:
                val = False
                if e.state > 0:
                    val = True
                if e.ev_type == 'Key':
                    self.on_key_data({'type': 'button', 'name': e.code, 'val': val})
                elif e.ev_type == 'Absolute':
                    self.on_key_data({'type': 'stick', 'name': e.code, 'val': e.state})

        except UnpluggedError as e:
            print(e)
        except UnknownEventCode as e:
            # print(e)
            self.buffer = {}

    def on_key_data(self, data):
        if data is None:
            return
        self.buffer[data['name']] = {'type': data['type'], 'name': data['name'], 'val': data['val']}
        self.packet_recv(self.buffer)

    def finish(self):
        pass

class GenericControllerParser:
    @staticmethod
    def readStick(input):
        return float((input - 128)) / 128.0

    @staticmethod
    def readFromPacket(sender, packet):
        state = ControllerStateBuilder()
        for key in packet:
            p = packet[key]

            # map buttons to nintendospy names
            if p['type'] == 'button':
                state.setButton(GENERIC_CONTROLLER_BTN[p['name']], p['val'])
            elif p['type'] == 'stick':
                # check for dpad
                if p['name'] == 'ABS_HAT0X':
                    if p['val'] == 0:
                        state.setButton('left', False)
                        state.setButton('right', False)
                    elif p['val'] == 1:
                        state.setButton('right', True)
                        state.setButton('left', False)
                    elif p['val'] == -1:
                        state.setButton('left', True)
                        state.setButton('right', False)
                elif p['name'] == 'ABS_HAT0Y':
                    if p['val'] == 0:
                        state.setButton('up', False)
                        state.setButton('down', False)
                    elif p['val'] == 1:
                        state.setButton('down', True)
                        state.setButton('up', False)
                    elif p['val'] == -1:
                        state.setButton('up', True)
                        state.setButton('down', False)
                elif p['name'] == 'ABS_X':
                    state.setAnalog('x', GenericControllerParser.readStick(p['val']))
                elif p['name'] == 'ABS_Y':
                    state.setAnalog('y', GenericControllerParser.readStick(p['val']))
                elif p['name'] == 'ABS_Z':
                    state.setAnalog('rx', GenericControllerParser.readStick(p['val']))
                elif p['name'] == 'ABS_RZ':
                    state.setAnalog('ry', GenericControllerParser.readStick(p['val']))

        return state.build()

GENERIC_CONTROLLER_BTN = {
    'BTN_THUMB': 'b0',
    'BTN_THUMB2': 'b1',
    'BTN_TRIGGER': 'b2',
    'BTN_TOP': 'b3',
    'BTN_PINKIE': 'b5',
    'BTN_TOP2': 'b4',
    'BTN_BASE4': 'b7',
    'BTN_BASE3': 'b6',

    # analogs
    'BTN_BASE6': 'b9',
    'BTN_BASE5': 'b8',

    'BTN_BASE2': 'b10',
    'BTN_BASE': 'b11'
}

# TODO map trigger buttons z
