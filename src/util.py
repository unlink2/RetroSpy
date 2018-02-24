

def parseColorStr(colstr):
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
