from ControllerState import ControllerStateBuilder
from util import readByte


class Nintendo64:
    def __init__(self):
        self.PACKET_SIZE = 32

        self.BUTTONS = ['a', 'b', 'z', 'start', 'up', 'down', 'left', 'right',
                        None, None, 'l', 'r', 'cup', 'cdown', 'cleft', 'cright']

        def readStick(input):
            return (input - 128) / 128

        def readFromPacket(packet):
            if(len(packet) < self.PACKET_SIZE):
                return None

            state = ControllerStateBuilder()

            for i in range(0, len(self.BUTTONS)):
                if self.BUTTONS[i] is None:
                    continue

                state.setButton(self.BUTTONS[i], packet[i] != 0x00)

            state.setAnalog('stick_x', self.readStick(readByte(packet, len(self.BUTTONS))))
            state.setAnalog('stick_y', self.readStick(readByte(packet, len(self.BUTTONS + 8))))
            return state.build()
