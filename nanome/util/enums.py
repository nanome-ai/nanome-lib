from . import IntEnum
#TODO normalize styling

class AtomRenderingMode(IntEnum):
    BallStick = 0
    Stick = 1
    Wire = 2
    VanDerWaals = 3
    Point = 4
    BFactor = 5
    Adaptive = 6

class Kind(IntEnum):
    Unknown = 0
    CovalentSingle = 1
    CovalentDouble = 2
    CovalentTriple = 3
    Aromatic = 4

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

class PluginListButtonType(IntEnum):
    run = 0
    advanced_settings = 1

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

class ToolTipPositioning(IntEnum):
    top_right = 0
    top = 1
    top_left = 2
    left = 3
    bottom_left = 4
    bottom = 5
    bottom_right = 6
    right = 7
    center = 8

class StreamType(IntEnum):
    position = 0
    color = 1
    scale = 2
    label = 3
    complex_position_rotation = 4
    shape_position = 5
    shape_color = 6
    sphere_shape_radius = 7

class StreamDataType(IntEnum):
    float = 0
    byte = 1
    string = 2

class StreamDirection(IntEnum):
    writing = 0
    reading = 1

class LoadFileErrorCode(IntEnum):
    no_error = 0
    loading_failed = 1

class VolumeType(IntEnum):
    default = 0
    density = 1
    density_diff = 2
    cryo_em = 3
    electrostatic = 4

class VolumeVisualStyle(IntEnum):
    Mesh = 0
    FlatSurface = 1
    SmoothSurface = 2

class ExportFormats(IntEnum):
    Nanome = 0
    PDB = 1
    SDF = 2
    MMCIF = 3
    SMILES = 4

class ShapeType(IntEnum):
    Sphere = 0
    Line = 1
    Label = 2

class ShapeAnchorType(IntEnum):
    Workspace = 0
    Complex = 1
    Atom = 2

class ColorScheme(IntEnum):
    #None = 0 this one is on nanome but does nothing
    Residue = 1
    Occupancy = 2
    BFactor = 3
    Element = 4
    Rainbow = 5
    Chain = 6
    DonorAcceptor = 7
    SecondaryStructure = 8
    Monochrome = 9
    YRBHydrophobicity = 10
    Hydrophobicity = 11
    IMGT = 12
    Kabat = 13
    Chothia = 14

class ColorSchemeTarget(IntEnum):
    AtomBond = 0
    Ribbon = 1
    Surface = 2
    All = 3

class SkyBoxes(IntEnum):
    Unknown = -1
    BlueSkyAndClouds = 0
    Sunset = 1
    BlueSkyAndGround = 2
    Black = 3
    White = 4
    Graydient = 5
