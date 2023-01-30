from . import *

from .base import Base  # noqa: F401
from .atom import Atom  # noqa: F401
from .bond import Bond  # noqa: F401
from .residue import Residue  # noqa: F401
from .chain import Chain  # noqa: F401
from .molecule import Molecule  # noqa: F401
from .complex import Complex  # noqa: F401
from .workspace import Workspace  # noqa: F401
from .substructure import Substructure  # noqa: F401

from . import client, io, messages, callbacks
from nanome.util import simple_callbacks
from nanome._internal.enums import Commands, Messages

registered_commands = [
    (Commands.workspace_response, messages.ReceiveWorkspace(), simple_callbacks.simple_callback_arg),
    (Commands.complex_add, messages.ComplexAddedRemoved(), callbacks.complex_added),
    (Commands.complex_remove, messages.ComplexAddedRemoved(), callbacks.complex_removed),
    (Commands.complex_list_response, messages.ReceiveComplexList(), simple_callbacks.simple_callback_arg),
    (Commands.complexes_response, messages.ReceiveComplexes(), callbacks.receive_complexes),
    (Commands.structures_deep_update_done, messages.UpdateStructuresDeepDone(), simple_callbacks.simple_callback_no_arg),
    (Commands.add_to_workspace_done, messages.AddToWorkspace(), simple_callbacks.simple_callback_arg),
    (Commands.position_structures_done, messages.PositionStructuresDone(), simple_callbacks.simple_callback_no_arg),
    (Commands.dssp_add_done, messages.AddDSSP(), simple_callbacks.simple_callback_arg),
    (Commands.bonds_add_done, messages.AddBonds(), simple_callbacks.simple_callback_arg),
    (Commands.complex_updated, messages.ComplexUpdated(), callbacks.complex_updated),
    (Commands.selection_changed, messages.SelectionChanged(), callbacks.selection_changed),
    (Commands.compute_hbonds_done, messages.ComputeHBonds(), simple_callbacks.simple_callback_no_arg),
    (Commands.substructure_response, messages.RequestSubstructure(), simple_callbacks.simple_callback_arg),
]

registered_messages = [
    (Messages.workspace_update, messages.UpdateWorkspace()),
    (Messages.structures_deep_update, messages.UpdateStructures(False)),
    (Messages.structures_shallow_update, messages.UpdateStructures(True)),
    (Messages.workspace_request, messages.RequestWorkspace()),
    (Messages.complex_list_request, messages.RequestComplexList()),
    (Messages.add_to_workspace, messages.AddToWorkspace()),
    (Messages.complexes_request, messages.RequestComplexes()),
    (Messages.bonds_add, messages.AddBonds()),
    (Messages.dssp_add, messages.AddDSSP()),
    (Messages.structures_zoom, messages.PositionStructures()),
    (Messages.structures_center, messages.PositionStructures()),
    (Messages.hook_complex_updated, messages.ComplexUpdatedHook()),
    (Messages.hook_selection_changed, messages.SelectionChangedHook()),
    (Messages.compute_hbonds, messages.ComputeHBonds()),
    (Messages.substructure_request, messages.RequestSubstructure()),
    (Messages.apply_color_scheme, messages.ApplyColorScheme()),
]
