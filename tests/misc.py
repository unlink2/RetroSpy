import unittest
import util


class TestMisc(unittest.TestCase):
    def test_readByte_unsigned(self):
        self.assertEqual(util.readByte([1, 0, 0, 0, 0, 0, 0, 0], 0, False), 128)

    def test_readByte_singed(self):
        self.assertEqual(util.readByte([1, 0, 0, 0, 0, 0, 0, 0], 0, True), -128)

    def test_setBit(self):
        self.assertEqual(util.setBit(0, 1), 2)

    def test_unsetBit(self):
        self.assertEqual(util.unsetBit(2, 1), 0)

    def test_readBit(self):
        self.assertEqual(util.readBit(2, 1), 1)

    def test_toggleBit(self):
        self.assertEqual(util.toggleBit(2, 1), 0)
        self.assertEqual(util.toggleBit(0, 1), 2)

    def test_parse_color(self):
        test_col_dict = {
                'r': 255,
                'g': 255,
                'b': 255,
                'a': 255
        }

        self.assertEqual(util.parseColorStr('ffffff', False), test_col_dict)
        self.assertEqual(util.parseColorStr('#ffffff'), '#ffffff')
        self.assertEqual(util.parseColorStr('ffffff'), '#ffffff')

