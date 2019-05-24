from . import IntEnum

class AtomRenderingMode(IntEnum):
    BallStick = 0
    Stick = 1
    Wire = 2
    VanDerWaals = 3
    Point = 4

class Kind(IntEnum):
    CovalentSingle = 1
    CovalentDouble = 2
    CovalentTriple = 3
    Hydrogen = 4
    HydrogenWater = 5

class PaddingTypes(IntEnum):
    fixed = 0
    ratio = 1

class SizingTypes(IntEnum):
    expand = 0
    fixed = 1
    ratio = 2

class LayoutTypes(IntEnum):
    vertical = 0
    horizontal = 1