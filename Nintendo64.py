from ControllerState import ControllerStateBuilder
from util import readByte


class Nintendo64:
    @staticmethod
    def readStick(input):
        return float((input - 128)) / 128.0

    @staticmethod
    def readFromPacket(packet):
        if(len(packet) < Nintendo64.PACKET_SIZE):
            return None

        state = ControllerStateBuilder()

        for i in range(0, len(Nintendo64.BUTTONS)):
            if Nintendo64.BUTTONS[i] is None:
                continue

            state.setButton(Nintendo64.BUTTONS[i], packet[i] != 0x00)

        state.setAnalog('stick_x', Nintendo64.readStick(readByte(packet, len(Nintendo64.BUTTONS))))
        state.setAnalog('stick_y', Nintendo64.readStick(readByte(packet, len(Nintendo64.BUTTONS) + 8)))

        return state.build()


Nintendo64.PACKET_SIZE = 31

Nintendo64.BUTTONS = ['a', 'b', 'z', 'start', 'up', 'down', 'left', 'right',
                None, None, 'l', 'r', 'cup', 'cdown', 'cleft', 'cright']
