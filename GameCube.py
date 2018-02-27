from ControllerState import ControllerStateBuilder
from util import readByte


class GameCube:
    def __init__(self):
        self.PACKET_SIZE = 64

        self.BUTTONS = [None, None, None, 'start', 'y', 'x', 'b', 'a', None,
                        'l', 'r', 'z', 'up', 'down', 'right', 'left']

        def readStick(input):
            return (input - 128) / 128

        def readTrigger(input):
            return input / 256

        def readFromPacket(packet):
            if(len(packet) < self.PACKET_SIZE):
                return None

            state = ControllerStateBuilder()

            for i in range(0, len(self.BUTTONS)):
                if self.BUTTONS[i] is None:
                    continue

                state.setButton(self.BUTTONS[i], packet[i] != 0x00)

            state.setAnalog('lstick_x', self.readStick(readByte(packet, len(self.BUTTONS))))
            state.setAnalog('lstick_y', self.readStick(readByte(packet, len(self.BUTTONS + 8))))
            state.setAnalog('cstick_x', self.readStick(readByte(packet, len(self.BUTTONS + 16))))
            state.setAnalog('cstick_y', self.readStick(readByte(packet, len(self.BUTTONS + 24))))
            state.setAnalog('trig_l', self.readStick(readByte(packet, len(self.BUTTONS + 32))))
            state.setAnalog('trig_r', self.readStick(readByte(packet, len(self.BUTTONS + 40))))
            return state.build()
