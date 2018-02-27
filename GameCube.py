from ControllerState import ControllerStateBuilder
from util import readByte


class GameCube:
    @staticmethod
    def readStick(input):
        return float((input - 128)) / 128.0

    @staticmethod
    def readTrigger(input):
        return input / 256.0

    @staticmethod
    def readFromPacket(packet):
        if(len(packet) < GameCube.PACKET_SIZE):
            return None
        state = ControllerStateBuilder()

        for i in range(0, len(GameCube.BUTTONS)):
            if GameCube.BUTTONS[i] is None:
                continue

            state.setButton(GameCube.BUTTONS[i], packet[i] != 0x00)

        state.setAnalog('lstick_x', GameCube.readStick(readByte(packet, len(GameCube.BUTTONS))))
        state.setAnalog('lstick_y', GameCube.readStick(readByte(packet, len(GameCube.BUTTONS) + 8)))
        state.setAnalog('cstick_x', GameCube.readStick(readByte(packet, len(GameCube.BUTTONS) + 16)))
        state.setAnalog('cstick_y', GameCube.readStick(readByte(packet, len(GameCube.BUTTONS) + 24)))
        state.setAnalog('trig_l', GameCube.readTrigger(readByte(packet, len(GameCube.BUTTONS) + 32)))
        state.setAnalog('trig_r', GameCube.readTrigger(readByte(packet, len(GameCube.BUTTONS) + 40)))

        return state.build()


GameCube.PACKET_SIZE = 64

GameCube.BUTTONS = [None, None, None, 'start', 'y', 'x', 'b', 'a', None,
                    'l', 'r', 'z', 'up', 'down', 'right', 'left']
