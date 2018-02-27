from ControllerState import ControllerStateBuilder

class SuperNESandNES:
    def __init__(self):
        self.BUTTONS_NES = ['a', 'b', 'select', 'start', 'up', 'down',
                            'left', 'right']

        self.BUTTONS_SNES = ['b', 'y', 'select', 'start', 'up', 'down', 'left',
                             'right', 'a', 'x', 'l', 'r', None, None, None, None]

    def readPacketButtons(self, packet, buttons):
        if len(packet) < len(buttons):
            return None

        state = ControllerStateBuilder()

        for i in range(0, len(buttons)):
            if buttons[i] is None:
                continue
            state.setButton(buttons[i], packet[i] != 0x00)

        return state.build()

    def readFromPacket_NES(self, packet):
        return self.readPacketButtons(packet, self.BUTTONS_NES)

    def readFromPacket_SNES(self, packet):
        reutnr self.readPacketButtons(packet, self.BUTTONS_SNES)
