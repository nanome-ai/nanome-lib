import nanome
from nanome.util import Logs
import sys
import time
import random
import struct
import math
from nanome.api.structure import *
from nanome.util import Vector3, Quaternion, Matrix
# Config

NAME = "ControllerTracking"
DESCRIPTION = "A plugin to demonstrate and test controller tracking."
CATEGORY = "User Tracking"
HAS_ADVANCED_OPTIONS = False

# Plugin


def rand_float(lower, upper):
    lower = max(-340282346638528859811704183484516925440, lower)
    upper = min(340282346638528859811704183484516925440, upper)
    dbl = random.uniform(lower, upper)
    flt = struct.unpack('f', struct.pack('f', dbl))[0]
    return flt


def rand_pos():
    return Vector3(rand_float(-5, 5), rand_float(0, 2), rand_float(-5, 5))


def random_quaternion():
    # double x,y,z, u,v,w, s
    x = rand_float(-1, 1)
    y = rand_float(-1, 1)
    z = x * x + y * y
    while(z > 1):
        x = rand_float(-1, 1)
        y = rand_float(-1, 1)
        z = x * x + y * y
    u = rand_float(-1, 1)
    v = rand_float(-1, 1)
    w = u * u + v * v
    while(w > 1):
        u = rand_float(-1, 1)
        v = rand_float(-1, 1)
        w = u * u + v * v
    s = math.sqrt((1 - z) / w)
    return Quaternion(x, y, s * u, s * v)


def rand_scale():
    scale = rand_float(.5, 1)
    return Vector3(scale, scale, scale)


class ControllerTrackingPlugin(nanome.PluginInstance):
    def start(self):
        self.make_tracking_atoms()
        self.make_menu()
        import time
        time.sleep(5)
        Logs.debug("requesting complexes")
        self.request_complex_list(self.connect_complexes)

    def make_menu(self):
        self.menu = nanome.ui.Menu()
        self.menu_position = Vector3()
        self.menu_rotation = Quaternion()
        self.menu_scale = Vector3()
        self.last = time.time()
        self.outstanding = True
        self.update_menu(self.menu)
        self.request_menu_transform(0, lambda _1, _2, _3: None)
        self.set_menu_transform(0, self.menu_position, self.menu_rotation, self.menu_scale)
        self.request_menu_transform(0, self.check_menu_stats)

    def check_menu_stats(self, pos, rot, scale):
        self.outstanding = False
        if not self.menu_position.equals(pos) or not self.menu_rotation.equals(rot) or not self.menu_scale.equals(scale):
            Logs.error("Menu not where it should be!")
            Logs.error(self.menu_position, pos)
            Logs.error(self.menu_rotation, rot)
            Logs.error(self.menu_scale, scale)
        else:
            Logs.debug("passed menu check")

    def update(self):
        if self.outstanding == False:
            curr = time.time()
            if curr - self.last > 3:
                self.outstanding = True
                self.last = curr
                self.menu_position = rand_pos()
                self.menu_rotation = random_quaternion()
                self.menu_scale = rand_scale()
                self.set_menu_transform(0, self.menu_position, self.menu_rotation, self.menu_scale)
                self.request_menu_transform(0, self.check_menu_stats)
        return super().update()

    def make_tracking_atoms(self):
        workspace = Workspace()
        self.world_matrix = workspace.get_workspace_to_world_matrix()
        self.workspace_matrix = workspace.get_world_to_workspace_matrix()
        self.head_complex = self.build_simple_complex("head", nanome.util.Color.Red())
        self.left_complex = self.build_simple_complex("left", nanome.util.Color.Blue())
        self.right_complex = self.build_simple_complex("right", nanome.util.Color.Green())
        workspace.add_complex(self.head_complex)
        workspace.add_complex(self.left_complex)
        workspace.add_complex(self.right_complex)
        Logs.debug("sending a workspace")
        self.update_workspace(workspace)

    def connect_complexes(self, complexes):
        Logs.debug("received some complexes", len(complexes))
        for complex in complexes:
            if complex.name == "head":
                self.head_complex = complex
            elif complex.name == "left":
                self.left_complex = complex
            elif complex.name == "right":
                self.right_complex = complex
        self.request_controller_transforms(self.received)

    def build_simple_complex(self, name, color):
        new_complex = Complex()
        new_complex.name = name
        new_molecule = Molecule()
        new_chain = Chain()
        new_residue = Residue()
        new_atom1 = Atom()
        new_atom2 = Atom()
        new_bond = Bond()
        new_complex.add_molecule(new_molecule)
        new_molecule.add_chain(new_chain)
        new_chain.add_residue(new_residue)
        new_residue.add_atom(new_atom1)
        new_residue.add_atom(new_atom2)
        new_residue.add_bond(new_bond)
        new_bond.atom1 = new_atom1
        new_bond.atom2 = new_atom2
        new_atom2.position = Vector3(0, 0, 1)
        new_atom1.atom_color = color
        new_atom2.atom_color = color
        return new_complex

    def received(self, head_position, head_rotation, left_controller_position, left_controller_rotation, right_controller_position, right_controller_rotation):
        self.head_complex.position = self.workspace_matrix * head_position
        new_rotation = self.workspace_matrix * Matrix.from_quaternion(head_rotation)
        self.head_complex.rotation = Quaternion.from_matrix(new_rotation)
        self.left_complex.position = self.workspace_matrix * left_controller_position
        new_rotation = self.workspace_matrix * Matrix.from_quaternion(left_controller_rotation)
        self.left_complex.rotation = Quaternion.from_matrix(new_rotation)
        self.right_complex.position = self.workspace_matrix * right_controller_position
        new_rotation = self.workspace_matrix * Matrix.from_quaternion(right_controller_rotation)
        self.right_complex.rotation = Quaternion.from_matrix(new_rotation)
        self.update_structures_shallow([self.head_complex, self.left_complex, self.right_complex])
        self.request_controller_transforms(self.received)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, ControllerTrackingPlugin)
