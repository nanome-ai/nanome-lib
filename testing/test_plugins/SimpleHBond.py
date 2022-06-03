import sys
import time
import nanome

minimum_bond_distance = 3
maximum_angstrom_distance = 3

# Config

NAME = "Test HBonds"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False

# Plugin


class SimpleHBond(nanome.PluginInstance):
    def start(self):
        print("Start Simple HBond Plugin")

    @staticmethod
    def _is_good_element(atom, current_element=None):
        if atom.symbol != 'H' and atom.symbol != 'O':
            return False
        if current_element == atom.symbol:
            return False
        return True

    @staticmethod
    def _check_atom(atom, original_atom, original_residue, depth, visited_atoms):
        visited_atoms.append(atom)
        # If we traveled at least minimum_bond_distance and distance is under maximum_angstrom_distance, we might have a HBond here
        if depth >= minimum_bond_distance \
                and nanome.util.Vector3.distance(atom.position, original_atom.position) <= maximum_angstrom_distance \
                and SimpleHBond._is_good_element(atom, original_atom.symbol):
            new_bond = nanome.structure.Bond()
            new_bond.kind = nanome.structure.Bond.Kind.Hydrogen
            new_bond.atom1 = original_atom
            new_bond.atom2 = atom
            original_residue.bonds.append(new_bond)
        # Check all bonds related to current atom
        for bond in original_residue.bonds:
            if bond.kind == nanome.structure.Bond.Kind.Hydrogen:
                continue
            if bond.atom1.index == atom.index:
                other_atom = bond.atom2
            elif bond.atom2.index == atom.index:
                other_atom = bond.atom1
            else:
                continue
            found = [x for x in visited_atoms if x.index == other_atom.index]
            if len(found) == 0:
                SimpleHBond._check_atom(other_atom, original_atom, original_residue, depth + 1, visited_atoms)

    @staticmethod
    def _check_atom_without_bonds(atom, workspace, original_residue, visited_atoms):
        for complex in workspace.complexes:
            for molecule in complex.molecules:
                for chain in molecule.chains:
                    for residue in chain.residues:
                        for current_atom in residue.atoms:
                            if SimpleHBond._is_good_element(current_atom, atom.symbol) == False:
                                continue
                            found = [x for x in visited_atoms if x.index == current_atom.index]
                            if len(found) == 0:
                                if nanome.util.Vector3.distance(atom.position, current_atom.position) <= maximum_angstrom_distance:
                                    new_bond = nanome.structure.Bond()
                                    new_bond.kind = nanome.structure.Bond.Kind.Hydrogen
                                    new_bond.atom1 = atom
                                    new_bond.atom2 = current_atom
                                    original_residue.bonds.append(new_bond)

    @staticmethod
    def _remove_hbonds(workspace):
        removed_hbonds = False
        for complex in workspace.complexes:
            for molecule in complex.molecules:
                for chain in molecule.chains:
                    for residue in chain.residues:
                        for i, b in reversed(list(enumerate(residue.bonds))):
                            if b.kind == nanome.structure.Bond.Kind.Hydrogen:
                                del residue.bonds[i]
                                removed_hbonds = True
        return removed_hbonds

    def on_workspace_received(self, workspace):
        if SimpleHBond._remove_hbonds(workspace):
            print("HBonds removed")
        else:
            for complex in workspace.complexes:
                for molecule in complex.molecules:
                    for chain in molecule.chains:
                        for residue in chain.residues:
                            for atom in residue.atoms:
                                if atom.selected == False:
                                    continue
                                if SimpleHBond._is_good_element(atom):
                                    visited_atoms = []
                                    SimpleHBond._check_atom(atom, atom, residue, 0, visited_atoms)
                                    SimpleHBond._check_atom_without_bonds(atom, workspace, residue, visited_atoms)
            nanome.util.Logs.debug("HBonds added")
        self.update_workspace(workspace)

    def on_run(self):
        self.request_workspace(self.on_workspace_received)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SimpleHBond)
