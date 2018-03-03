from GameCube import GameCube
from Nintendo64 import Nintendo64
from MegaDrive import MegaDrive
from SuperNESandNES import SuperNESandNES
from SerialControllerReader import SerialControllerReader
from PreviewReader import PreviewReader, PreviewParser
from KeyboardReader import KeyboardReader, KeyboardParser
import time
import sched
from threading import Thread


class InputSource:
    def __init__(self, type_tag, name, requries_comport, requires_id, controllerreader):
        self.type_tag = type_tag
        self.name = name
        self.requries_comport = requries_comport
        self.requires_id = requires_id
        self.controllerreader = controllerreader   # Controller Class

    def makeControllerReader(self, controllerid=0, comport='', preview=False):
        # TODO send arduino firmware mode over serial and implement reading it in firmware
        if self.type_tag == 'preview' or preview:
            self.controllerreader = PreviewReader(PreviewParser.readFromPacket)
        elif self.type_tag == 'nes':
            self.controllerreader = SerialControllerReader(comport, SuperNESandNES.readFromPacket_NES)
            self.schedule_serial_mode(self.type_tag)
        elif self.type_tag == 'snes':
            self.controllerreader = SerialControllerReader(comport, SuperNESandNES.readFromPacket_SNES)
            self.schedule_serial_mode(self.type_tag)
        elif self.type_tag == 'n64':
            self.controllerreader = SerialControllerReader(comport, Nintendo64.readFromPacket)
            self.schedule_serial_mode(self.type_tag)
        elif self.type_tag == 'gamecube':
            self.controllerreader = SerialControllerReader(comport, GameCube.readFromPacket)
            self.schedule_serial_mode(self.type_tag)
        elif self.type_tag == 'megadrive':
            self.controllerreader = SerialControllerReader(comport, MegaDrive.readFromPacket)
            self.schedule_serial_mode(self.type_tag)
        elif self.type_tag == 'megadrive6':
            self.controllerreader = SerialControllerReader(comport, MegaDrive.readFromPacket)
            self.schedule_serial_mode(self.type_tag)
        elif self.type_tag == 'keyboard':
            self.controllerreader = KeyboardReader(KeyboardParser.readFromPacket)
        else:
            raise Exception('Unable to make build reader')

    def schedule_serial_mode(self, type_tag):
        self.thread = Thread(target=self.send_serial_mode, args=(type_tag,))
        self.thread.start()

    def send_serial_mode(self, type_tag):
        time.sleep(2)
        self.controllerreader.serial.serial_write('M' + str(InputSource.ARDUINO_MODEPINS[self.type_tag]))

    @staticmethod
    def makeInputSource(type_tag):
        if type_tag in InputSource.ALL:
            if type_tag == 'nes':
                return InputSource(type_tag, 'NES', True, False, None)
            elif type_tag == 'snes':
                return InputSource(type_tag, 'SNES', True, False, None)
            elif type_tag == 'n64':
                return InputSource(type_tag, 'Nintendo 64', True, False, None)
            elif type_tag == 'gamecube':
                return InputSource(type_tag, 'GameCube', True, False, None)
            elif type_tag == 'megadrive':
                return InputSource('megadrive', 'MegaDrive3 Button', True, False, None)
            elif type_tag == 'megadrive6':
                return InputSource('megadrive6', 'MegaDrive 6 Button', True, False, None)
            elif type_tag == 'preview':
                return InputSource('preview', 'Preview', False, False, None)
            elif type_tag == 'keyboard':
                return InputSource('keyboard', 'Keyboard', False, False, None)

        return None  # return None in case of fail


InputSource.ALL = ['nes', 'snes', 'n64', 'gamecube', 'megadrive', 'preview', 'keyboard', 'megadrive6']
InputSource.ARDUINO_MODEPINS = {'nes': 4, 'snes': 0, 'n64': 1, 'gamecube': 2, 'megadrive': 3, 'megadrive6': 5}
