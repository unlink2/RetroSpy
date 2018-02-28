import os
import keyboard


def sendKeyToOS(key):
    # first we check for root or windows
    # print a warning if not root
    if os.geteuid() == 0 or os.name == 'nt':
        keyboard.press_and_release(key)
    else:
        print('[Warning]: to send keypresses you must either use Windows or run this script as root!')


def parseColorStr(colstr, return_hex=True):
    if return_hex:
        return '#' + colstr
    red = ""
    green = ""
    blue = ""

    if len(colstr) == 3:
        red = colstr[0]
        green = colstr[1]
        blue = colstr[2]
    elif len(colstr) == 6:
        red = colstr[0:2]
        green = colstr[2:4]
        blue = colstr[4:6]
    else:
        raise Exception('Unable to parse color string.')
    return {'r': int(red, 16), 'g': int(green, 16), 'b': int(blue, 16),
            'a': 255}


# converts array of at least 8 bytes to an integer
# implementation of SignalTool
def readByte(packet, offset, singed=False):
    val = 0
    for i in range(0, 8):
        if (packet[i + offset] & 0x0F) != 0:
            val = val | (1 << 7 - i)
    if singed and val > 127:
        return (256 - val) * (-1)
    return val


def setBit(num, bit):
    return num | 1 << bit


def unsetBit(num, bit):
    return num & ~(1 << bit)


def toggleBit(num, bit):
    return num ^ (1 << bit)


def readBit(num, bit):
    mask = 1 << bit
    masked_n = num & mask
    thebit = masked_n >> bit
    return thebit
