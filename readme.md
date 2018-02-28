#RetroSpy

This is a port of [NintendoSpy](https://github.com/jaburns/NintendoSpy) to make it multiplatform.

The goal of this project is to maintain compatability with the original Application.
It also implements an experimental Sega MegaDrive (Genesis) 3 button controller mode.

Current implementation status:

  SNES: Untested
  NES: Untested
  MegaDrive: 3 button only
  Nintend 64: Working correctly
  GameCube: Working correctly
  XInput: Not implemented
  Generic Controller: Not implemented


It depends on python 3.X and the following libraries

    pip install pySerial
    pip install pillow
    pip install xmltodict
    pip install axel
    pip install keyboard

New skin tag:
Buttons can have an onkeydown attribute with a key combination.
If you run this script as root, or are using windows, it will then send the specified key to the OS as a keyboard input.

More documentation to come soon.
