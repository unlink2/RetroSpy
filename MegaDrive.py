from ControllerState import ControllerStateBuilder
from util import readBit

class MegaDrive:
    def __init__(self):
        self.PACKET_SIZE = 2

        # buttosn for when 7 is high
        self.BUTTONS_0 = [None, None, 'up', 'down', 'left', 'right', 'b', 'c']
        self.BUTTONS_1 = [None, None, None, None, None, None, 'a', 'start']

    def readFromPacket(self, packet):
        if(len(packet) < self.PACKET_SIZE):
            return None

        state = ControllerStateBuilder()

        # data starts at bit 2
        for i in range(0, 8):
            if self.BUTTONS_0[i] is None:
                continue

            state.setButton(self.BUTTONS_0[i], readBit(packet[0], i) != 0x01)

        for i in range(0, 8):
            if self.BUTTONS_1[i] is None:
                continue
            state.setButton(self.BUTTONS_1[i], readBit(packet[1], i) != 0x01)

        return state.build()
