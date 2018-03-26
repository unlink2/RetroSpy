import unittest
import util


class TestMisc(unittest.TestCase):
    def test_readByte_unsigned(self):
        self.assertEqual(util.readByte([1, 0, 0, 0, 0, 0, 0, 0], 0, False), 128)

    def test_readByte_singed(self):
        self.assertEqual(util.readByte([1, 0, 0, 0, 0, 0, 0, 0], 0, True), -128)

