from GameCube import GameCube
from Nintendo64 import Nintendo64
from MegaDrive import MegaDrive
from SuperNESandNES import SuperNESandNES
from SerialControllerReader import SerialControllerReader
from PreviewReader import PreviewReader, PreviewParser

class InputSource:
    def __init__(self, type_tag, name, requries_comport, requires_id, controllerreader):
        self.type_tag = type_tag
        self.name = name
        self.requries_comport = requries_comport
        self.requires_id = requires_id
        self.controllerreader = controllerreader   # Controller Class

    def makeControllerReader(self, controllerid=0, comport='', preview=False):
        if self.type_tag == 'preview' or preview:
            self.controllerreader = PreviewReader(PreviewParser.readFromPacket)
        elif self.type_tag == 'nes':
            self.controllerreader = SerialControllerReader(comport, SuperNESandNES.readFromPacket_NES)
        elif self.type_tag == 'snes':
            self.controllerreader = SerialControllerReader(comport, SuperNESandNES.readFromPacket_SNES)
        elif self.type_tag == 'n64':
            self.controllerreader = SerialControllerReader(comport, Nintendo64.readFromPacket)
        elif self.type_tag == 'gamecube':
            self.controllerreader = SerialControllerReader(comport, GameCube.readFromPacket)
        elif self.type_tag == 'megadrive':
            self.controllerreader = SerialControllerReader(comport, MegaDrive.readFromPacket)
        else:
            raise Exception('Unable to make build reader')

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
                return InputSource('megadrive', 'MegaDrive', True, False, None)
            elif type_tag == 'preview':
                return InputSource('preview', 'Preview', False, False, None)

        return None  # return None in case of fail


InputSource.ALL = ['nes', 'snes', 'n64', 'gamecube', 'megadrive', 'preview']
