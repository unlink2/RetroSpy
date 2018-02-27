class InputSource:
    def __init__(self, type_tag, name, requries_comport, requires_id, buildreader):
        self.type_tag = type_tag
        self.name = name
        self.requries_comport = requries_comport
        self.requires_id = requires_id
        self.buildreader = buildreader  # callback function

# static variables
# TODO insert Readers here


InputSource.NES = InputSource('nes', 'NES', True, False, None)
InputSource.SNES = InputSource('snes', 'SNES', True, False, None)
InputSource.N64 = InputSource('n64', 'Nintendo 64', True, False, None)
InputSource.GAMECUBE = InputSource('gamecube', 'GameCube', True, False, None)
InputSource.MEGADRIVE = InputSource('megadrive', 'MegaDrive', True, False, None)

InputSource.ALL = [InputSource.NES, InputSource.SNES, InputSource.N64,
                   InputSource.GAMECUBE, InputSource.MEGADRIVE]
