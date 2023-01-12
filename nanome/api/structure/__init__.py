from . import *

from .base import Base
from .atom import Atom
from .bond import Bond
from .residue import Residue
from .chain import Chain
from .molecule import Molecule
from .complex import Complex
from .workspace import Workspace
from .substructure import Substructure

from . import client, io, messages, callbacks
from nanome.api import callbacks as base_callbacks
from nanome._internal.enums import Commands

registered_commands = [
    (Commands.workspace_response, messages.ReceiveWorkspace(), base_callbacks.simple_callback_arg),
    (Commands.complex_add, messages.ComplexAddedRemoved(), callbacks.complex_added),
    (Commands.complex_remove, messages.ComplexAddedRemoved(), callbacks.complex_removed),
    (Commands.complex_list_response, messages.ReceiveComplexList(), base_callbacks.simple_callback_arg),
    (Commands.complexes_response, messages.ReceiveComplexes(), callbacks.receive_complexes),
    (Commands.structures_deep_update_done, messages.UpdateStructuresDeepDone(), base_callbacks.simple_callback_no_arg),
    (Commands.add_to_workspace_done, messages.AddToWorkspace(), base_callbacks.simple_callback_arg),
    (Commands.position_structures_done, messages.PositionStructuresDone(), base_callbacks.simple_callback_no_arg),
    (Commands.dssp_add_done, messages.AddDSSP(), base_callbacks.simple_callback_arg),
    (Commands.bonds_add_done, messages.AddBonds(), base_callbacks.simple_callback_arg),
    (Commands.complex_updated, messages.ComplexUpdated(), callbacks.complex_updated),
    (Commands.selection_changed, messages.SelectionChanged(), callbacks.selection_changed),
    (Commands.compute_hbonds_done, messages.ComputeHBonds(), base_callbacks.simple_callback_no_arg),
    (Commands.substructure_response, messages.RequestSubstructure(), base_callbacks.simple_callback_arg),
]