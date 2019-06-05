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

class RibbonMode(IntEnum):
    SecondaryStructure = 0
    AdaptiveTube = 1
    Coil = 2

class SecondaryStructure(IntEnum):
    Unknown = 0
    Coil = 1
    Sheet = 2
    Helix = 3

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
    
class ScalingOptions(IntEnum):
    stretch = 0
    fill = 1
    fit = 2

class NotificationTypes(IntEnum):
    message = 0
    success = 1
    warning = 2
    error = 3

class HorizAlignOptions(IntEnum):
    Left = 0
    Middle = 1
    Right = 2
    
class VertAlignOptions(IntEnum):
    Top = 0
    Middle = 1
    Bottom = 2