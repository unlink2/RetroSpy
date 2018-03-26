import unittest
from Nintendo64 import Nintendo64
from ControllerState import ControllerStateBuilder


class TestNintendo64(unittest.TestCase):
    def test_N64_ReadPacket_down(self):
        test_builder = ControllerStateBuilder()
        test_builder.setButton('up', True)
        test_builder.setButton('down', True)
        test_builder.setButton('left', True)
        test_builder.setButton('right', True)
        test_builder.setButton('a', True)
        test_builder.setButton('b', True)
        test_builder.setButton('z', True)
        test_builder.setButton('start', True)
        test_builder.setButton('l', True)
        test_builder.setButton('r', True)
        test_builder.setButton('cup', True)
        test_builder.setButton('cdown', True)
        test_builder.setButton('cleft', True)
        test_builder.setButton('cright', True)

        test_builder.setAnalog('stick_x', -1.0)
        test_builder.setAnalog('stick_y', -1.0)

        test_packet = Nintendo64.readFromPacket([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 0, 0, 0, 0, 0, 0])

        self.assertEqual(test_packet.analogs, test_builder.build().analogs)
        self.assertEqual(test_packet.buttons, test_builder.build().buttons)

    def test_N64_ReadPacket_up(self):
        test_builder = ControllerStateBuilder()
        test_builder.setButton('up', False)
        test_builder.setButton('down', False)
        test_builder.setButton('left', False)
        test_builder.setButton('right', False)
        test_builder.setButton('a', False)
        test_builder.setButton('b', False)
        test_builder.setButton('z', False)
        test_builder.setButton('start', False)
        test_builder.setButton('l', False)
        test_builder.setButton('r', False)
        test_builder.setButton('cup', False)
        test_builder.setButton('cdown', False)
        test_builder.setButton('cleft', False)
        test_builder.setButton('cright', False)

        test_builder.setAnalog('stick_x', 0.0)
        test_builder.setAnalog('stick_y', 0.0)

        test_packet = Nintendo64.readFromPacket([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0])

        self.assertEqual(test_packet.analogs, test_builder.build().analogs)
        self.assertEqual(test_packet.buttons, test_builder.build().buttons)


