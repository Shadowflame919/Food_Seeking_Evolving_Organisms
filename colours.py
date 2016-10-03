import random


BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)

RED     = ( 255,   0,   0)
ORANGE  = ( 255, 128,   0)
YELLOW  = ( 255, 255,   0)
LIME    = ( 128, 255,   0)
AQUA    = (   0, 255, 255)
BLUE    = (   0,   0, 255)
PURPLE  = ( 255,   0, 255)

LIGHT_RED   = (255, 179, 179)
DARK_RED    = (139,   0,   0)

LIGHT_BLUE  = ( 127, 127, 255)
DARK_BLUE   = (   0,   0, 127)


LIGHT_PAPER = ( 248, 236, 194)
PAPER       = ( 228, 216, 174)
DARK_PAPER  = ( 208, 196, 154)

def GREY(c):
    return (c,c,c)

def GREEN(c):
    return (0,c,0)

def orgColour(rgb=None):
    if rgb == None:
        c1 = random.randrange(256)
        c2 = random.randrange(255 - c1)
        c3 = 255 - c1 - c2
        rgb = [c1,c2,c3]
        random.shuffle(rgb)
        return rgb
    else:
        colourMix = [0,1,2]
        random.shuffle(colourMix)

        changeAmount = random.randrange(10)
        if rgb[colourMix[0]] + changeAmount > 255:
            changeAmount = 255 - rgb[colourMix[0]]
        rgb[colourMix[0]] += changeAmount
        if rgb[colourMix[1]] - changeAmount < 0:
            rgb[colourMix[2]] -= changeAmount - rgb[colourMix[1]]
            changeAmount = rgb[colourMix[1]]
        rgb[colourMix[1]] -= changeAmount

        return rgb

            



