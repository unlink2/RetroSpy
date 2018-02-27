from ControllerState import ControllerStateBuilder

class SuperNESandNES:
    @staticmethod
    def readPacketButtons(packet, buttons):
        if len(packet) < len(buttons):
            return None

        state = ControllerStateBuilder()

        for i in range(0, len(buttons)):
            if buttons[i] is None:
                continue
            state.setButton(buttons[i], packet[i] != 0x00)

        return state.build()

    @staticmethod
    def readFromPacket_NES(packet):
        return SuperNESandNES.readPacketButtons(packet, SuperNESandNES.BUTTONS_NES)

    @staticmethod
    def readFromPacket_SNES(packet):
        return SuperNESandNES.readPacketButtons(packet, SuperNESandNES.BUTTONS_SNES)


SuperNESandNES.BUTTONS_NES = ['a', 'b', 'select', 'start', 'up', 'down',
                    'left', 'right']

SuperNESandNES.BUTTONS_SNES = ['b', 'y', 'select', 'start', 'up', 'down', 'left',
                     'right', 'a', 'x', 'l', 'r', None, None, None, None]
