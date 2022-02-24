import nanome
import sys
import time

# Config

NAME = "Deep Update Plugin"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Test"
HAS_ADVANCED_OPTIONS = False

# Plugin


class DeepUpdatePlugin(nanome.PluginInstance):
    def start(self):
        print("Start DeepUpdateWorkspace Plugin")

    def on_workspace_received(self, workspace):
        nanome.util.Logs.debug("RUNNINNGANSDGNASDNFASDFA")
        redcomplex = True
        redmolecule = True
        redchain = True
        redresidue = True
        redbond = True
        redatom = True
        dirty_structures = []
        for complex in workspace.complexes:
            if redcomplex:
                print("complex colored")
                redcomplex = False
                dirty_structures.append(complex)
                DeepUpdatePlugin.red_complex(complex)
                continue
            for molecule in complex.molecules:
                if redmolecule:
                    print("molecule colored")
                    redmolecule = False
                    dirty_structures.append(molecule)
                    DeepUpdatePlugin.red_molecule(molecule)
                    continue
                for chain in molecule.chains:
                    if redchain:
                        print("chain colored")
                        redchain = False
                        dirty_structures.append(chain)
                        DeepUpdatePlugin.red_chain(chain)
                        continue
                    for residue in chain.residues:
                        if redresidue:
                            print("residue colored")
                            redresidue = False
                            dirty_structures.append(residue)
                            DeepUpdatePlugin.red_residue(residue)
                            continue
                        for bond in residue.bonds:
                            if redbond:
                                print("bond colored")
                                redbond = False
                                DeepUpdatePlugin.red_bond(bond)
                                continue
                        for atom in residue.atoms:
                            if redatom:
                                print("atom colored")
                                redatom = False
                                dirty_structures.append(atom)
                                DeepUpdatePlugin.red_atom(atom)
                                continue
        nanome.util.Logs.debug("XXXXXXXXXXXXXXXXXXXXXXXX")
        self.update_structures_deep(dirty_structures)

    @staticmethod
    def red_atom(atom):
        atom.surface_rendering = True
        atom.surface_color = nanome.util.Color.Red()

    @staticmethod
    def red_bond(bond):
        DeepUpdatePlugin.red_atom(bond.atom1)
        DeepUpdatePlugin.red_atom(bond.atom2)

    @staticmethod
    def red_residue(residue):
        for atom in residue.atoms:
            DeepUpdatePlugin.red_atom(atom)

    @staticmethod
    def red_chain(chain):
        for residue in chain.residues:
            DeepUpdatePlugin.red_residue(residue)

    @staticmethod
    def red_molecule(molecule):
        for chain in molecule.chains:
            DeepUpdatePlugin.red_chain(chain)

    @staticmethod
    def red_complex(complex):
        for molecule in complex.molecules:
            DeepUpdatePlugin.red_molecule(molecule)

    def on_run(self):
        self.request_workspace(self.on_workspace_received)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, DeepUpdatePlugin)
