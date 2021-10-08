import os
import nanome
from nanome.api import structure as struct
from nanome.util import enums
from nanome.util import Logs
import sys
import time

# Config

NAME = "Sand Box"
DESCRIPTION = "A plugin that can be edited freely for testing."
CATEGORY = ["Simple Actions", "Test", "Sandbox"]
HAS_ADVANCED_OPTIONS = False
INTEGRATIONS = [enums.Integrations.structure_prep, enums.Integrations.minimization]
PERMISSIONS = [enums.Permissions.local_files_access]

# Plugin


class SandBox(nanome.PluginInstance):
    def start(self):
        self.room.set_skybox(nanome.util.enums.SkyBoxes.Graydient)

    def on_run(self):
        self.apply_color_scheme(enums.ColorScheme.BFactor, enums.ColorSchemeTarget.All, False)
        self.request_workspace(self.work)

    def work(self, workspace):
        (proteins, ligands, solvents) = self.categorize_atoms(workspace)
        self.color_categories(proteins, ligands, solvents)
        self.update_workspace(workspace)

    def categorize_atoms(self, workspace):
        unsorted_atoms = []
        ligands = []
        proteins = []
        solvents = []

        for complex in workspace.complexes:
            for bond in complex.bonds:
                bond.cleaved = False
            for atom in complex.atoms:
                atom.starred = False
                if atom.is_het:
                    for bond in atom.bonds:
                        self.cleave_bond(bond)
                unsorted_atoms.append(atom)

        connected_components = []
        while len(unsorted_atoms) > 0:
            connected_components.append(self.bonded_mass(unsorted_atoms[0], unsorted_atoms))
        Logs.debug("Connected Components:" + str(len(connected_components)))
        for component in connected_components:
            heavy_count = self.count_heavy_atoms(component)
            if heavy_count > 100:
                proteins.extend(component)
            elif heavy_count < 6:
                solvents.extend(component)
            elif self.contains_starred_atoms(component):
                ligands.extend(component)
            else:
                proteins.extend(component)
        return proteins, ligands, solvents

    def star_atoms(self, atom):
        for bond in atom.bonds:
            if bond.atom1.is_het:
                return
            if bond.atom2.is_het:
                return
        atom.starred = True

    def cleave_bond(self, bond):
        if bond.atom1.is_het and not bond.atom2.is_het:
            bond.cleaved = True
            bond.atom1.starred = True
            bond.atom2.starred = True
            return
        if not bond.atom1.is_het and bond.atom2.is_het:
            bond.cleaved = True
            bond.atom1.starred = True
            bond.atom2.starred = True
            return

    def bonded_mass(self, starting_atom, remaining_atoms):
        try:
            remaining_atoms.remove(starting_atom)
        except:
            return []
        mass = []
        for bond in starting_atom.bonds:
            if bond.cleaved:
                continue
            if starting_atom == bond.atom1:
                next_atom = bond.atom2
            else:
                next_atom = bond.atom1

            if next_atom in remaining_atoms:
                mass.extend(self.bonded_mass(bond.atom2, remaining_atoms))
        mass.append(starting_atom)
        return mass

    def count_heavy_atoms(self, component):
        count = 0
        for atom in component:
            if (atom.symbol != 'H'):
                count += 1
        return count

    def contains_starred_atoms(self, component):
        for atom in component:
            if atom.starred:
                return True
        return False

    def color_categories(self, proteins, ligands, solvents):
        for atom in proteins:
            atom.atom_color = nanome.util.Color.Red()
        for atom in ligands:
            atom.atom_color = nanome.util.Color.Green()
        for atom in solvents:
            atom.atom_color = nanome.util.Color.Blue()


def __init__(self):
    pass


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SandBox, integrations=INTEGRATIONS, permissions=PERMISSIONS)
