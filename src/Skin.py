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
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0  # image dimensions
        self.target_backgrounds = []  # list of strings
        self.ignore_backgrounds = []


class Background:
    def __init__(self):
        self.name = ""  # string
        self.image = None
        self.color = {'r': 0, 'g': 0, 'b': 0, 'a': 255}
        self.width = 0
        self.height = 0


class Detail:
    def __init__(self):
        self.name = ""
        self.element_config = ElementConfig()


class Button:
    def __init__(self):
        self.name = ""
        self.element_config = ElementConfig()


class RangeButton:
    def __init__(self):
        self.name = ""
        self.element_config = ElementConfig()
        self.fromF = 0.0
        self.toF = 0.0  # floats


class AnalogStick:
    def __init__(self):
        self.element_config = ElementConfig()
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
        self.element_config = ElementConfig()
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

        cwd = os.getcwd()
        skinpath = os.path.join(cwd, folder)

        if not Path(os.path.join(skinpath, 'skin.xml')).exists():
            raise Exception("Could not find skin.xml for skin at " + skinpath)

        doc = {}
        with open(os.path.join(skinpath, 'skin.xml')) as fd:
            doc = xmltodict.parse(fd.read())

        self.name = self.readStringAttr(doc['skin'], '@name')
        self.author = self.readStringAttr(doc['skin'], '@author')

        self.type = None
        # find the apropriate Input Type
        for source in InputSource.ALL:
            if source.type_tag == self.readStringAttr(doc['skin'], '@type'):
                self.type = source

        if self.type is None:
            raise Exception('Illegal value specified for skin \
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
                if '@width' in bg and bg['@width'] > 0:
                    width = bg['@width']
                if '@height' in bg and bg['@height'] > 0:
                    height = bg['@height']
            else:
                if '@width' in bg and bg['@width'] > 0:
                    width = bg['@width']
                if '@height' in bg['@height']:
                    height = bg['@height']

                if width > 0 and height > 0:
                    raise Exception('Element \'background\' should either define\
                    \'image\' with optionally \'width\' and \'height\'\
                    or both \'width\' and \'height\'.')

            newbg = Background()

            newbg.name = self.readStringAttr(bg, '@name')
            newbg.image = image
            newbg.color = self.readColorAttr(bg, '@color', False)
            newbg.width = width
            newbg.height = height

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
                raise Exception('Rangebutton \'from\' field cannot be greater\
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
                newa.direction == DOWN
            elif directionattr == 'left':
                newa.direction == LEFT
            elif directionattr == 'right':
                newa.direction == RIGHT
            else:
                raise Exception('Element \'analog\' attribute \'direction\' \
                has illegal value. Valid \
                values are \'up\', \'down\', \'left\', \'right\'.')

            newa.config = self.parseStandardConfig(skinpath, a)
            newa.xname = self.readStringAttr(a, '@name')
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
            raise Exception('Skin must contain at least one \
            \'' + attrname + '\'.')

        return allele

    def readStringAttr(self, elem, attrname, required=True):
        if attrname in elem:
            return elem[attrname]
        elif required:
            raise Exception('Required attribute \'' + attrname + '\' \
            not found.')
        return

    def readArrayAttr(self, elem, attrname, required=True):
        if attrname in elem:
            return elem[attrname].split(';')
        elif required:
            raise Exception('Required attribute \'' + attrname + '\' \
            not found.')
        else:
            return []

    def readColorAttr(self, elem, attrname, required=True):
        if attrname in elem:
            # parse color
            colstr = elem[attrname]
            return util.parseColorStr(colstr)
        elif required:
            raise Exception('Required attribute \'' + attrname + '\' \
            not found.')
        return {'r': 0, 'g': 0, 'b': 0, 'a': 255}

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
            width = elem['@width']

        if heightattr > 0:
            height = elem['@height']

        x = self.readIntAttr(elem, '@x')
        y = self.readIntAttr(elem, '@y')

        targetbgs = self.readArrayAttr(elem, '@target', False)
        ignorebgs = self.readArrayAttr(elem, '@ignore', False)

        newelemcfg = ElementConfig()
        newelemcfg.x = x
        newelemcfg.y = y
        newelemcfg.image = image
        newelemcfg.width = width
        newelemcfg.height = height
        newelemcfg.target_backgrounds = targetbgs
        newelemcfg.ignore_backgrounds = ignorebgs

        return newelemcfg


# ==================================================================#
# Helper function/calss                                             #
# ==================================================================#


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
        except Exception as e:
            skins.pare_errors.append(e)

    return skins
