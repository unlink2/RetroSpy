#!/usr/bin/env python

# Retro Controller input display software
# Copyright (C) 2018  Lukas Krickl

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Email: lukaskrickl@gmail.com

# This is a multiplatform port of the input display viewer NintendoSpy
# The original NintendoSpy was written in C# and does not compile well
# on platforms other than Windows
# This port is made to be compatible with the original program as much as
# possible.
# All Skins and Controllers (barring XInput?) will be supproted.

from SerialMonitor import SerialMonitor
from SetupWindow import SetupWindow
from CommandlineUI import CommandlineUI
from serial.tools import list_ports
import argparse
import util

def main():
    SetupWindow()

def debugMain(comport, device_type):
    CommandlineUI(comport, device_type=device_type)


def parseArgs():
    parser = argparse.ArgumentParser(description='Controller Input Display Software')
    parser.add_argument('--ports', dest='ports',
                        action='store_true',
                        help='Lists all available com ports.')
    parser.add_argument('--nox', dest='nox',
                        action='store',
                        help='Turn on command line mode. This will dump all button states to stdout\
                        Usage: --nox <comport> <device type>',
                        nargs=2)

    args = parser.parse_args()
    if args.ports:
        ports = list_ports.comports()
        print("Available com ports: ")
        for p in ports:
            print(p)

    if args.nox is None:
        main()
    else:
        debugMain(args.nox[0], args.nox[1])


parseArgs()
