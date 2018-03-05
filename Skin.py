import os
from pathlib import Path
import xmltodict
from PIL import Image
import collections
import util
from InputSource import InputSource


class ElementConfig:
    def __init__(self):
        self.image = None  # tk image
        self.image_path = ''
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0  # image dimensions
        self.target_backgrounds = []  # list of strings
        self.ignore_backgrounds = []
        self.image_crop = None
        self.on_keydown = None


class Background:
    def __init__(self):
        self.name = ""  # string
        self.image = None
        self.image_path = ''
        self.color = '#000000'
        self.width = 0
        self.height = 0


class Detail:
    def __init__(self):
        self.name = ""
        self.config = ElementConfig()


class Button:
    def __init__(self):
        self.name = ""
        self.config = ElementConfig()


class RangeButton:
    def __init__(self):
        self.name = ""
        self.config = ElementConfig()
        self.fromF = 0.0
        self.toF = 0.0  # floats


class AnalogStick:
    def __init__(self):
        self.config = ElementConfig()
        self.xname = ""
        self.yname = ""  # strings
        self.xrange = 0
        self.yrange = 0  # int
        self.xreverse = False
        self.yreverse = False  # bool


UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


class AnalogTrigger:
    def __init__(self):
        self.name = ""
        self.config = ElementConfig()
        self.direction = UP  # DirectionValue UP DOWN LEFT RIGHT
        self.is_reversed = False  # bool
        self.use_negative = False  # bool


class Skin:
    def __init__(self, folder):
        self.name = ""
        self.author = ""
        self.type = None  # InputSource (Not yet implemented)

        # just leaving those comments here
        # because we are keeping lists typesafe
        self.backgrounds = []  # list of backgrounds
        self.details = []  # list of details
        self.buttons = []  # list of buttons
        self.rangebuttons = []  # list of rangebuttons
        self.analogsticks = []  # list of analogsticks
        self.analogtriggers = []  # list of analogtriggers

        self.name = ''
        self.author = ''
        self.type_str = ''
        self.type = None

        cwd = os.getcwd()
        skinpath = os.path.join(cwd, folder)

        doc = {'skin': {}}
        self.doc = doc
        self.skinpath = skinpath
        self.load()

    def load(self):
        skinpath = self.skinpath
        if not Path(os.path.join(skinpath, 'skin.xml')).exists():
            raise SkinParseException("Could not find skin.xml for skin at " + skinpath)

        doc = {'skin': {}}
        with open(os.path.join(skinpath, 'skin.xml')) as fd:
            doc = xmltodict.parse(fd.read())

        self.load_xml_dict(doc)

    def load_xml_dict(self, doc):
        skinpath = self.skinpath
        self.name = self.readStringAttr(doc['skin'], '@name')
        self.author = self.readStringAttr(doc['skin'], '@author')

        # find the apropriate Input Type
        self.type_str = self.readStringAttr(doc['skin'], '@type')
        self.type = InputSource.makeInputSource(self.readStringAttr(doc['skin'], '@type'))

        if self.type is None:
            raise SkinParseException('Illegal value specified for skin \
            attribute\'type\'. ' + skinpath)

        backgrounds = self.getAllElements(doc['skin'], 'background', True)

        for bg in backgrounds:
            imagepath = None

            imagepath = self.readStringAttr(bg, '@image', False)
            image = None
            width = 0
            height = 0
            if imagepath is not None or imagepath != "":
                # TODO find a way to deal with stupid windows escaped paths
                image = Image.open(os.path.join(skinpath, imagepath))
                width, height = image.size
                if '@width' in bg and int(bg['@width']) > 0:
                    width = bg['@width']
                if '@height' in bg and int(bg['@height']) > 0:
                    height = bg['@height']
            else:
                if '@width' in bg and int(bg['@width']) > 0:
                    width = bg['@width']
                if '@height' in bg and int(bg['@height']) > 0:
                    height = bg['@height']

                if width > 0 and height > 0:
                    raise SkinParseException('Element \'background\' should either define\
                    \'image\' with optionally \'width\' and \'height\'\
                    or both \'width\' and \'height\'.')

            newbg = Background()

            newbg.name = self.readStringAttr(bg, '@name')
            newbg.image = image
            newbg.color = self.readColorAttr(bg, '@color', False)
            newbg.width = width
            newbg.height = height
            newbg.image_path = imagepath

            self.backgrounds.append(newbg)

        details = self.getAllElements(doc['skin'], 'detail')

        for d in details:
            newd = Detail()
            newd.config = self.parseStandardConfig(skinpath, d)
            newd.name = self.readStringAttr(d, '@name')

            self.details.append(newd)

        buttons = self.getAllElements(doc['skin'], 'button')

        for b in buttons:
            newb = Button()
            newb.config = self.parseStandardConfig(skinpath, b)
            newb.name = self.readStringAttr(b, '@name')

            self.buttons.append(newb)

        rangebuttons = self.getAllElements(doc['skin'], 'rangebutton')

        for rb in rangebuttons:
            fromf = self.readFloatAttr(rb, '@from')
            tof = self.readFloatAttr(rb, '@to')

            if fromf > tof:
                raise SkinParseException('Rangebutton \'from\' field cannot be greater\
                than \'to\' field.')

            newrb = RangeButton()
            newrb.config = self.parseStandardConfig(skinpath, rb)
            newrb.name = self.readStringAttr(rb, '@name')
            newrb.fromF = fromf
            newrb.toF = tof

            self.rangebuttons.append(newrb)

        sticks = self.getAllElements(doc['skin'], 'stick')

        for s in sticks:
            news = AnalogStick()
            news.config = self.parseStandardConfig(skinpath, s)
            news.xname = self.readStringAttr(s, '@xname')
            news.yname = self.readStringAttr(s, '@yname')
            news.xrange = self.readIntAttr(s, '@xrange')
            news.yrange = self.readIntAttr(s, '@yrange')
            news.xreverse = self.readBoolAttr(s, '@xreverse')
            news.yreverse = self.readBoolAttr(s, '@yreverse')

            self.analogsticks.append(news)

        analogs = self.getAllElements(doc['skin'], 'analog')

        for a in analogs:
            directionattr = self.readStringAttr(a, '@direction')

            newa = AnalogTrigger()

            if directionattr == 'up':
                newa.direction = UP
            elif directionattr == 'down':
                newa.direction = DOWN
            elif directionattr == 'left':
                newa.direction = LEFT
            elif directionattr == 'right':
                newa.direction = RIGHT
            else:
                raise SkinParseException('Element \'analog\' attribute \'direction\' \
                has illegal value. Valid \
                values are \'up\', \'down\', \'left\', \'right\'.')

            newa.config = self.parseStandardConfig(skinpath, a)
            newa.name = self.readStringAttr(a, '@name')
            newa.is_reversed = self.readBoolAttr(a, '@reverse')
            newa.use_negative = self.readBoolAttr(a, '@usenegative')

            self.analogtriggers.append(newa)

    def getAllElements(self, elem, attrname, required=False):
        if attrname not in elem:
            return []

        allele = elem[attrname]

        if type(allele) is collections.OrderedDict:
            allele = [allele]

        if len(allele) < 1 and required:
            raise SkinParseException('Skin must contain at least one \
            \'' + attrname + '\'.')

        return allele

    def readStringAttr(self, elem, attrname, required=True):
        if attrname in elem:
            return elem[attrname]
        elif required:
            raise SkinParseException('Required attribute \'' + attrname + '\' \
            not found.')
        return None

    def readArrayAttr(self, elem, attrname, required=True):
        if attrname in elem:
            if elem[attrname] == '':
                return []
            return elem[attrname].split(';')
        elif required:
            raise SkinParseException('Required attribute \'' + attrname + '\' \
            not found.')
        else:
            return []

    def readColorAttr(self, elem, attrname, required=True):
        if attrname in elem:
            # parse color
            colstr = elem[attrname]
            try:
                return util.parseColorStr(colstr)
            except Exception as e:
                raise SkinParseException(str(e) + ' ' + self.name)
        elif required:
            raise SkinParseException('Required attribute \'' + attrname + '\' \
            not found.')
        return '#000000'

    def readIntAttr(self, elem, attrname):
        if attrname in elem:
            return int(elem[attrname])
        return 0

    def readFloatAttr(self, elem, attrname):
        if attrname in elem:
            return float(elem[attrname])
        return 0.0

    def readBoolAttr(self, elem, attrname, dfault=False):
        if attrname in elem:
            if elem[attrname] == 'true':
                return True
            elif elem[attrname] == 'false':
                return False
        return dfault

    def parseStandardConfig(self, skinpath, elem):
        imageattr = self.readStringAttr(elem, '@image')

        image = Image.open(os.path.join(skinpath, imageattr))

        width, height = image.size

        widthattr = self.readIntAttr(elem, '@width')
        heightattr = self.readIntAttr(elem, '@height')
        if widthattr > 0:
            width = widthattr

        if heightattr > 0:
            height = heightattr

        x = self.readIntAttr(elem, '@x')
        y = self.readIntAttr(elem, '@y')

        targetbgs = self.readArrayAttr(elem, '@target', False)
        ignorebgs = self.readArrayAttr(elem, '@ignore', False)

        on_keydown = self.readStringAttr(elem, '@onkeydown', False)

        newelemcfg = ElementConfig()
        newelemcfg.x = x
        newelemcfg.y = y
        newelemcfg.image = image
        newelemcfg.image_crop = image
        newelemcfg.width = width
        newelemcfg.height = height
        newelemcfg.target_backgrounds = targetbgs
        newelemcfg.ignore_backgrounds = ignorebgs
        newelemcfg.on_keydown = on_keydown
        newelemcfg.image_path = imageattr

        return newelemcfg

    # this unparses all the xmls and writes them back. if no path is chosen it
    # writes to previous

    def write_to_xml(self, path=None):
        if path is None:
            path = self.skinpath
        with open(os.path.join(path, 'skin.xml'), 'w') as fd:
            fd.write(self.skin_to_xml_string())

    def skin_to_xml_string(self):
        # empty skin xml
        doc = {'skin': {
            '@author': self.author,
            '@name': self.name,
            '@type': self.type_str
        }}

        for bg in self.backgrounds:
            if 'background' not in doc['skin']:
                doc['skin']['background'] = []

            bgdict = {}
            bgdict['@name'] = bg.name
            bgdict['@image'] = bg.image_path
            bgdict['@color'] = bg.color.replace('#', '')
            bgdict['@width'] = bg.width
            bgdict['@height'] = bg.height

            doc['skin']['background'].append(bgdict)

        for d in self.details:
            if 'detail' not in doc['skin']:
                doc['skin']['detail'] = []

            detaildict = self.default_config_to_dict(d)
            detaildict['@name'] = d.name

            doc['skin']['detail'].append(detaildict)

        for b in self.buttons:
            if 'button' not in doc['skin']:
                doc['skin']['button'] = []

            buttondict = self.default_config_to_dict(b)
            buttondict['@name'] = b.name

            doc['skin']['button'].append(buttondict)

        for rb in self.rangebuttons:
            if 'rangebutton' not in doc['skin']:
                doc['skin']['rangebutton'] = []

            rbdict = self.default_config_to_dict(rb)
            rbdict['@name'] = rb.name
            rbdict['@to'] = rb.toF
            rbdict['@from'] = rb.fromF

            doc['skin']['rangebutton'].append(rbdict)

        for s in self.analogsticks:
            if 'stick' not in doc['skin']:
                doc['skin']['stick'] = []

            sdict = self.default_config_to_dict(s)
            sdict['@xname'] = s.xname
            sdict['@yname'] = s.yname
            sdict['@xrange'] = s.xrange
            sdict['@yrange'] = s.yrange

            if s.xreverse:
                sdict['@xreverse'] = 'true'
            else:
                sdict['@xreverse'] = 'false'
            if s.yreverse:
                sdict['@yreverse'] = 'true'
            else:
                sdict['@yreverse'] = 'false'

            doc['skin']['stick'].append(sdict)

        for a in self.analogtriggers:
            if 'analog' not in doc['skin']:
                doc['skin']['analog'] = []

            adict = self.default_config_to_dict(a)

            if a.direction == UP:
                adict['@direction'] = 'up'
            elif a.direction == DOWN:
                adict['@direction'] = 'down'
            elif a.direction == LEFT:
                adict['@direction'] = 'left'
            elif a.direction == RIGHT:
                adict['@direction'] = 'right'
            else:
                raise SkinParseException('Element \'analog\' has illegal \'direction\' value')

            adict['@name'] = a.name

            if a.is_reversed:
                adict['@reverse'] = 'true'
            else:
                adict['@reverse'] = 'false'

            if a.use_negative:
                adict['@usenegative'] = 'true'
            else:
                adict['@usenegative'] = 'false'

            doc['skin']['analog'].append(adict)

        return xmltodict.unparse(doc, pretty=True)

    def default_config_to_dict(self, element):
        dc = element.config
        d = {}

        d['@image'] = dc.image_path
        d['@x'] = dc.x
        d['@y'] = dc.y
        d['@width'] = dc.width
        d['@height'] = dc.height
        d['@target'] = ';'.join(str(x) for x in dc.target_backgrounds)
        d['@ignore'] = ';'.join(str(x) for x in dc.ignore_backgrounds)

        if dc.on_keydown is not None:
            d['@onkeydown'] = dc.on_keydown

        return d

    # returns class, type string
    def get_element(self, name):
        # loop all types
        for i in self.backgrounds:
            if i.name == name:
                return i, 'background'

        for i in self.buttons:
            if i.name == name:
                return i, 'button'

        for i in self.analogsticks:
            if i.xname == name or i.yname == name:
                return i, 'stick'

        for i in self.analogtriggers:
            if i.name == name:
                return i, 'trigger'

        for i in self.rangebuttons:
            if i.name == name:
                return i, 'rangebutton'

        for i in self.details:
            if i.name == name:
                return i, 'detail'

        return None, ''

# ==================================================================#
# Helper function/calss                                             #
# ==================================================================#


class SkinParseException(Exception):
    pass


class LoadResults:
    def __init__(self):
        self.skins_loaded = []
        self.pare_errors = []


def loadAllSkinsFromParentFolder(path):
    skins = LoadResults()

    for skindir in os.listdir(path):
        if skindir == '.' or skindir == '..':
            continue
        try:
            skins.skins_loaded.append(Skin(os.path.join(path, skindir)))
        except SkinParseException as e:
            skins.pare_errors.append(e)

    return skins
