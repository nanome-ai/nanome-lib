import nanome
from nanome.util import Logs
import sys
import time
from nanome.api import structure as struct
from nanome.util import Vector3
from nanome.util import Quaternion
# Config

NAME = "ControllerTracking"
DESCRIPTION = "A plugin to demonstrate and test controller tracking."
CATEGORY = "User Tracking"
HAS_ADVANCED_OPTIONS = False

# Plugin

class ControllerTrackingPlugin(nanome.PluginInstance):
    def start(self):
        self.make_tracking_atoms()
        self.request_complex_list(self.connect_complexes)

    def make_tracking_atoms(self):
        self.head_complex = self.build_simple_complex("head", nanome.util.Color.Red())
        self.left_complex = self.build_simple_complex("left", nanome.util.Color.Blue())
        self.right_complex = self.build_simple_complex("right", nanome.util.Color.Green())
        self.add_to_workspace([self.head_complex, self.left_complex, self.right_complex,])

    def connect_complexes(self, complexes):
        for complex in complexes:
            if complex.name == "head":
                self.head_complex = complex
            elif complex.name == "left": 
                self.left_complex = complex
            elif complex.name == "right": 
                self.right_complex = complex
        self.request_controller_transforms(self.received)

    def build_simple_complex(self, name, color):
        new_complex = struct.Complex()
        new_complex.name = name
        new_molecule = struct.Molecule()
        new_chain = struct.Chain()
        new_residue = struct.Residue()
        new_atom1 = struct.Atom()
        new_atom2 = struct.Atom()
        new_bond = struct.Bond()
        new_complex.add_molecule(new_molecule)
        new_molecule.add_chain(new_chain)
        new_chain.add_residue(new_residue)
        new_residue.add_atom(new_atom1)
        new_residue.add_atom(new_atom2)
        new_residue.add_bond(new_bond)
        new_bond.atom1 = new_atom1
        new_bond.atom2 = new_atom2
        new_atom2.position = Vector3(0,0,1)
        new_atom1.atom_color = color
        new_atom2.atom_color = color
        return new_complex

    def received(self, head_position, head_rotation, left_controller_position, left_controller_rotation, right_controller_position, right_controller_rotation):
        self.head_complex.position = head_position
        self.head_complex.rotation = head_rotation
        self.left_complex.position = left_controller_position
        self.left_complex.rotation = left_controller_rotation
        self.right_complex.position = right_controller_position
        self.right_complex.rotation = right_controller_rotation
        self.update_structures_shallow([self.head_complex, self.left_complex, self.right_complex])
        self.request_controller_transforms(self.received)

    def __init__(self):
        pass

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, ControllerTrackingPlugin)