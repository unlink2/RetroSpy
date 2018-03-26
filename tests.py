#!/usr/bin/env python
import unittest
from MegaDrive import MegaDrive
from ControllerState import ControllerStateBuilder


class TestMegaDrive(unittest.TestCase):
    def test_MD_ReadPacket(self):
        test_builder = ControllerStateBuilder()
        test_builder.setButton('up', True)
        test_builder.setButton('down', True)
        test_builder.setButton('left', True)
        test_builder.setButton('right', True)
        test_builder.setButton('a', True)
        test_builder.setButton('b', True)
        test_builder.setButton('c', True)
        test_builder.setButton('x', True)
        test_builder.setButton('y', True)
        test_builder.setButton('z', True)
        test_builder.setButton('start', True)
        test_builder.setButton('mode', True)

        test_packet = MegaDrive.readFromPacket([0, 0, 0])

        self.assertEqual(test_packet.buttons, test_builder.build().buttons)

if __name__ == '__main__':
    unittest.main()
