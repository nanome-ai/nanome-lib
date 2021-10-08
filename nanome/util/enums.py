from . import IntEnum
from .enum import auto
try:
    from nanome.util import reset_auto
except:
    def reset_auto():
        pass
import sys


class SubstructureType(IntEnum):
    """
    | The types of Substructures that can be parsed from a Molecule.
    """
    Unkown = 0
    Protein = 1
    Ligand = 2
    Solvent = 3


class AtomRenderingMode(IntEnum):
    """
    | Shape types an atom can be rendered as.
    | To be used with atom.atom_mode
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
    | Bond types.
    | To be used with bond.kind and elements of bond.kinds
    """
    Unknown = 0
    CovalentSingle = 1
    CovalentDouble = 2
    CovalentTriple = 3
    Aromatic = 4


class RibbonMode(IntEnum):
    """
    | Ribbon display modes.
    | To be used with structure.Residue().ribbon_mode
    """
    SecondaryStructure = 0
    AdaptiveTube = 1
    Coil = 2


class SecondaryStructure(IntEnum):
    """
    | Secondary structure types.
    | To be used with structure.Residue().secondary_structure
    """
    Unknown = 0
    Coil = 1
    Sheet = 2
    Helix = 3


class PaddingTypes(IntEnum):
    """
    | UI padding types.
    | To be used with ui.LayoutNode().padding_type
    """
    fixed = 0
    ratio = 1


class PluginListButtonType(IntEnum):
    """
    | Buttons on the plugin list, modifiable by the plugin itself.
    | To be used with plugin_instance.set_plugin_list_button
    """
    run = 0
    advanced_settings = 1


class SizingTypes(IntEnum):
    """
    | Ways in which a Layout Node can be sized within a UI layout.
    | To be used with ui.LayoutNode().sizing_type
    """
    expand = 0
    fixed = 1
    ratio = 2


class LayoutTypes(IntEnum):
    """
    | Orientation modes for Layout Nodes.
    | To be used with ui.LayoutNode().layout_orientation
    """
    vertical = 0
    horizontal = 1


class ScalingOptions(IntEnum):
    """
    | Ways for an image to scale.
    | To be used with ui.Image().scaling_option
    """
    stretch = 0
    fill = 1
    fit = 2


class NotificationTypes(IntEnum):
    """
    | Types of user notifications.
    | Each value exists as a method on nanome.util.Logs
    """
    message = 0
    success = 1
    warning = 2
    error = 3


class HorizAlignOptions(IntEnum):
    """
    | Horizontal alignment modes for text.
    | To be used with ui.Label().text_horizontal_align and ui.Button().horizontal_align
    """
    Left = 0
    Middle = 1
    Right = 2


class VertAlignOptions(IntEnum):
    """
    | Vertical alignment modes for text.
    | To be used with ui.Label().text_vertical_align and ui.Button().vertical_align
    """
    Top = 0
    Middle = 1
    Bottom = 2


class ToolTipPositioning(IntEnum):
    """
    | Ways in which a tooltip can appear on top of its Layout Node.
    | To be used with ui.Button().tooltip.positioning_target
    """
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
    | Object attributes and sets of attributes that can be streamed to Nanome.
    | To be used with plugin_instance.create_writing_stream and plugin_instance.create_reading_stream
    """
    position = 0
    color = 1
    scale = 2
    label = 3
    complex_position_rotation = 4
    shape_position = 5
    shape_color = 6
    sphere_shape_radius = 7


class StreamDataType(IntEnum):
    """
    | Stream datatypes.
    | Used internally
    """
    float = 0
    byte = 1
    string = 2


class StreamDirection(IntEnum):
    """
    | Stream directions (reading and writing).
    | Used internally
    """
    writing = 0
    reading = 1


class LoadFileErrorCode(IntEnum):
    """
    | Errors when loading files into Nanome.
    | Accessible via the first parameter of the 'done' callback for plugin_instance.send_files_to_load
    """
    no_error = 0
    loading_failed = 1


class VolumeType(IntEnum):
    """
    | Volume types visible within a complex.
    | To be used with _internal._volumetric._VolumeData()._type
    """
    default = 0
    density = 1
    density_diff = 2
    cryo_em = 3
    electrostatic = 4


class VolumeVisualStyle(IntEnum):
    """
    | Ways that a complex's volume can be displayed.
    | To be used with _internal._volumetric._VolumeProperties()._style
    """
    Mesh = 0
    FlatSurface = 1
    SmoothSurface = 2


class ExportFormats(IntEnum):
    """
    | File export formats.
    | To be used with plugin_instance.request_export
    """
    Nanome = 0
    PDB = 1
    SDF = 2
    MMCIF = 3
    SMILES = 4


class ShapeType(IntEnum):
    """
    | Types of shapes that can be created within Nanome.
    | Used internally
    """
    Sphere = 0
    Line = 1
    Label = 2
    Mesh = 3


class ShapeAnchorType(IntEnum):
    """
    | Object type to anchor a Shape to.
    | To be used with shapes.Shape().anchors
    """
    Workspace = 0
    Complex = 1
    Atom = 2


class ColorScheme(IntEnum):
    """
    | Color schemes for all structure representations.
    | To be used with plugin_instance.apply_color_scheme
    """
    # None = 0 this one is on nanome but does nothing
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
    APF = 15


class ColorSchemeTarget(IntEnum):
    """
    | Structure representations.
    | To be used with plugin_instance.apply_color_scheme
    """
    AtomBond = 0
    Ribbon = 1
    Surface = 2
    All = 3


class SkyBoxes(IntEnum):
    """
    | Preset skyboxes to show in a Nanome room
    | To be used with plugin_instance.room.set_skybox
    """
    Unknown = -1
    BlueSkyAndClouds = 0
    Sunset = 1
    BlueSkyAndGround = 2
    Black = 3
    White = 4
    Graydient = 5


class _CommandEnum(IntEnum):
    if sys.version_info >= (3, 6):  # Tmp hack
        # Override for auto()
        def _generate_next_value_(name, start, count, last_values):
            return IntEnum._generate_next_value_(name, 0, count, last_values)
    else:
        pass


class Integrations(_CommandEnum):
    # Tmp hack
    reset_auto()  # Not an enum

    hydrogen = auto()
    structure_prep = auto()
    calculate_esp = auto()
    minimization = auto()
    export_file = auto()
    export_locations = auto()
    generate_molecule_image = auto()
    import_file = auto()
    analysis = auto()
    interactions = auto()


class Permissions(_CommandEnum):
    # Tmp hack
    reset_auto()  # Not an enum

    local_files_access = auto()
