from . import IntEnum
#TODO normalize styling

class AtomRenderingMode(IntEnum):
    """
    | Enumerator for type of shape the atoms are rendered as.
    """
    BallStick = 0
    Stick = 1
    Wire = 2
    VanDerWaals = 3
    Point = 4
    BFactor = 5
    Adaptive = 6

class Kind(IntEnum):
    """
    | Enumerator for type of bond.
    """
    Unknown = 0
    CovalentSingle = 1
    CovalentDouble = 2
    CovalentTriple = 3
    Aromatic = 4

class RibbonMode(IntEnum):
    """
    | Enumerator for how the residue ribbon should be displayed
    """
    SecondaryStructure = 0
    AdaptiveTube = 1
    Coil = 2

class SecondaryStructure(IntEnum):
    """
    | Enumerator for type of secondary structure a residue has
    """
    Unknown = 0
    Coil = 1
    Sheet = 2
    Helix = 3

class PaddingTypes(IntEnum):
    """
    | Enumerator for type of padding in a layout for a menu
    """
    fixed = 0
    ratio = 1

class PluginListButtonType(IntEnum):
    """
    | Enumerator for generic plugin button types
    """
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
    """
    | Enumerator for type of stream to be made
    """
    position = 0
    color = 1
    scale = 2
    label = 3
    complex_position_rotation = 4
    shape_position_rotation = 5
    shape_color = 6
    sphere_shape_radius = 7

class StreamDataType(IntEnum):
    """
    | Enumerator for a stream's data type
    """
    float = 0
    byte = 1
    string = 2

class StreamDirection(IntEnum):
    """
    | Enumerator for the direction (writing or reading) that the stream is going in
    """
    writing = 0
    reading = 1

class LoadFileErrorCode(IntEnum):
    """
    | Enumerator for loading file errors
    """
    no_error = 0
    loading_failed = 1

class VolumeType(IntEnum):
    """
    | Enumerator for type of volume inside an object
    """
    default = 0
    density = 1
    density_diff = 2
    cryo_em = 3
    electrostatic = 4

class VolumeVisualStyle(IntEnum):
    """
    | Enumerator of how the volume is displayed
    """
    Mesh = 0
    FlatSurface = 1
    SmoothSurface = 2

class ExportFormats(IntEnum):
    """
    | Enumerator for export format with a specific extension.
    """
    Nanome = 0
    PDB = 1
    SDF = 2
    MMCIF = 3
    SMILES = 4

class ShapeType(IntEnum):
    """
    | Enumerator for shape types that are supported
    """
    Sphere = 0

class ShapeAnchorType(IntEnum):
    """
    | Enumerator to represent which object we are anchoring onto.
    """
    Workspace = 0
    Complex = 1
    Atom = 2

class ColorScheme(IntEnum):
    """
    | Enumerator for color schemes depending on the object
    """
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
    """
    | Enumerator to specify which target to color
    """
    AtomBond = 0
    Ribbon = 1
    Surface = 2
    All = 3

class SkyBoxes(IntEnum):
    """
    | Enumerator for type of skybox to show in a Nanome room
    """
    Unknown = -1
    BlueSkyAndClouds = 0
    Sunset = 1
    BlueSkyAndGround = 2
    Black = 3
    White = 4
    Graydient = 5
