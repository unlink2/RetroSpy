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
from updater import Updater
from inputs import devices
import sys
import os
from InputSource import InputSource


def main():
    SetupWindow()


def debugMain(comport, device_type):
    CommandlineUI(comport, device_type=device_type)


def cli_update():
    print('Current version: ', Updater.version_str(), '. Checking for updates...')
    util.updater.check_update()
    if util.updater.update_available:
        print('Update available on: ', util.updater.update_url, ' version: ', util.updater.new_ver)
        # util.updater.download()
        # util.updater.restart()
    else:
        print('No updates available!')


def parseArgs():
    parser = argparse.ArgumentParser(description='Controller Input Display Software')
    parser.add_argument('--ports', dest='ports',
                        action='store_true',
                        help='Lists all available com ports.')
    parser.add_argument('--about', dest='about',
                        action='store_true',
                        help='Print out information about the program')

    parser.add_argument('--version', dest='version', action='store_true', help='Displays version')

    parser.add_argument('--update', dest='update',
                        action='store_true',
                        help='Checks for updates and downloads from command line')
    parser.add_argument('--dump', dest='dump',
                        action='store',
                        help='Turn on command line mode. This will dump all button states to stdout\
                        Usage: --dump <comport> <device type>',
                        nargs=2)

    parser.add_argument('--nox', dest='nox', action='store_true', help='Prevents GUI from opening')

    args = parser.parse_args()
    util.cli_args = args
    if args.ports:
        ports = list_ports.comports()
        print("Available com ports: ")
        for p in ports:
            print(p)
        print('Available input devices: ')
        for d in devices.keyboards:
            print(d._device_path)
        #for d in devices.mice:
        #    print(d._device_path)
        print('Available gamepads: ')
        for d in devices.gamepads:
            print(d._device_path)
        print('Available input modes: ')
        for d in InputSource.ALL:
            print(d)

    if args.about:
        print(util.ABOUT_TEXT)

    if args.version:
        print(util.APPLICATION_NAME, ' version ', Updater.version_str())
        print('Reported OS: ', os.name)
        print('Reported python version: ', sys.version)

    if args.update:
        cli_update()

    if not args.nox:
        main()
    if args.dump is not None:
        debugMain(args.dump[0], args.dump[1])


parseArgs()
sys.exit(0)
