#!/usr/bin/env python
import unittest
from MegaDrive import MegaDrive
from ControllerState import ControllerStateBuilder
from tests.TestMegaDrive import TestMegaDrive
from tests.TestGameCube import TestGameCube
from tests.TestNintendo64 import TestNintendo64
from tests.misc import TestMisc


def run_test():
    unittest.main()

if __name__ == '__main__':
    run_test()
