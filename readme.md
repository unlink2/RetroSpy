# RetroSpy

[![Build Status](https://travis-ci.org/unlink2/RetroSpy.svg?branch=master)](https://travis-ci.org/unlink2/RetroSpy)

This is a port of [NintendoSpy](https://github.com/jaburns/NintendoSpy) to make it multiplatform.

The goal of this project is to maintain compatability with the original Application.
It also implements an experimental Sega MegaDrive (Genesis) 3 button controller mode.

Current implementation status:

   SNES: Untested
   NES: Untested
   MegaDrive: 3 button and 6 button
   Nintend 64: Working correctly
   GameCube: Working correctly
   XInput: Not implemented
   Generic Controller: partly implemented (Trigger buttons are not compatible)
   Keyboard: Implemented


It depends on python 3.X and the following libraries

    pip install pySerial
    pip install pillow
    pip install xmltodict
    pip install axel
    pip install keyboard
    pip install inputs

New skin tag:
Buttons can have an onkeydown attribute with a key combination.
If you run this script as root, or are using windows, it will then send the specified key to the OS as a keyboard input.

Every button tag can also include an action attribute. If action is set to a plugin's name the plugin's on_action method will be called.

More documentation to come soon.

## Note about Keyboard Input

This program can display keyboard inputs. It is therefore pretty easy to use this as a keylogger.
Please do not use it for malocious purposes.
