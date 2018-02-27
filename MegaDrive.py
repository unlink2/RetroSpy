from ControllerState import ControllerStateBuilder
from util import readBit


class MegaDrive:
    @staticmethod
    def readFromPacket(packet):
        if(len(packet) < MegaDrive.PACKET_SIZE):
            return None

        state = ControllerStateBuilder()

        # data starts at bit 2
        for i in range(0, 8):
            if MegaDrive.BUTTONS_0[i] is None:
                continue

            state.setButton(MegaDrive.BUTTONS_0[i], readBit(packet[0], i) != 0x01)

        for i in range(0, 8):
            if MegaDrive.BUTTONS_1[i] is None:
                continue
            state.setButton(MegaDrive.BUTTONS_1[i], readBit(packet[1], i) != 0x01)

        return state.build()


MegaDrive.PACKET_SIZE = 2

# buttosn for when 7 is high
MegaDrive.BUTTONS_0 = [None, None, 'up', 'down', 'left', 'right', 'b', 'c']
MegaDrive.BUTTONS_1 = [None, None, None, None, None, None, 'a', 'start']
