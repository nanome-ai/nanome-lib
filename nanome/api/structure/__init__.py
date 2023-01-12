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
from nanome.util import simple_callbacks 
from nanome._internal.enums import Commands

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