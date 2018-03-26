import unittest
from GameCube import GameCube
from ControllerState import ControllerStateBuilder


class TestGameCube(unittest.TestCase):
    def test_GCN_ReadPacket_down(self):
        test_builder = ControllerStateBuilder()
        test_builder.setButton('up', True)
        test_builder.setButton('down', True)
        test_builder.setButton('left', True)
        test_builder.setButton('right', True)
        test_builder.setButton('start', True)
        test_builder.setButton('y', True)
        test_builder.setButton('x', True)
        test_builder.setButton('b', True)
        test_builder.setButton('a', True)
        test_builder.setButton('l', True)
        test_builder.setButton('r', True)
        test_builder.setButton('z', True)

        # triggers never reach 1.0, this is max
        test_builder.setAnalog('lstick_x', 0.9921875)
        test_builder.setAnalog('lstick_y', 0.9921875)
        test_builder.setAnalog('cstick_x', 0.9921875)
        test_builder.setAnalog('cstick_y', 0.9921875)
        test_builder.setAnalog('trig_l', 0.99609375)
        test_builder.setAnalog('trig_r', 0.99609375)

        test_packet = GameCube.readFromPacket([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1])

        self.assertEqual(test_packet.analogs, test_builder.build().analogs)
        self.assertEqual(test_packet.buttons, test_builder.build().buttons)

    def test_GCN_ReadPacket_up(self):
        test_builder = ControllerStateBuilder()
        test_builder.setButton('up', False)
        test_builder.setButton('down', False)
        test_builder.setButton('left', False)
        test_builder.setButton('right', False)
        test_builder.setButton('start', False)
        test_builder.setButton('y', False)
        test_builder.setButton('x', False)
        test_builder.setButton('b', False)
        test_builder.setButton('a', False)
        test_builder.setButton('l', False)
        test_builder.setButton('r', False)
        test_builder.setButton('z', False)

        test_builder.setAnalog('lstick_x', -1.0)
        test_builder.setAnalog('lstick_y', -1.0)
        test_builder.setAnalog('cstick_x', -1.0)
        test_builder.setAnalog('cstick_y', -1.0)
        test_builder.setAnalog('trig_l', 0.0)
        test_builder.setAnalog('trig_r', 0.0)

        test_packet = GameCube.readFromPacket([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0])

        self.assertEqual(test_packet.analogs, test_builder.build().analogs)
        self.assertEqual(test_packet.buttons, test_builder.build().buttons)


