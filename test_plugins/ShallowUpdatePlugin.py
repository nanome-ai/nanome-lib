import nanome
import sys
import time
from nanome._internal._structure import _Bond

# Config

NAME = "Shallow Update Plugin"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False
NTS_ADDRESS = '127.0.0.1'
NTS_PORT = 8888

# Plugin

def count_structures(complex):
    molecule_counter = 0
    chain_counter = 0
    residue_counter = 0
    residue_counter = 0
    bond_counter = 0
    atom_counter = 0
    for molecule in complex.molecules:
        molecule_counter += 1
        for chain in molecule.chains:
            chain_counter += 1
            for residue in chain.residues:
                residue_counter += 1
                for atom in residue.atoms:
                    atom_counter += 1
                for bond in residue.bonds:
                    bond_counter +=1
    print("molecule_counter:",molecule_counter)
    print("chain_counter:",chain_counter)
    print("residue_counter:",residue_counter)
    print("residue_counter:",residue_counter)
    print("bond_counter:",bond_counter)
    print("atom_counter:",atom_counter)

class ShallowUpdatePlugin(nanome.PluginInstance):
    def start(self):
        print("Start ShallowUpdate Plugin")

#complex: name
#molecule: name
#chain: name
#residue: name
#bond: kind
#atom: name
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
                count_structures(complex)
                complex.name = "AAA"
                complex.boxed = True
                # redcomplex = False
                dirty_structures.append(complex)
                # continue
            for molecule in complex.molecules:
                if redmolecule:
                    print("molecule colored")
                    molecule.name = "BBB"
                    # redmolecule = False
                    dirty_structures.append(molecule)
                    # continue
                for chain in molecule.chains:
                    if redchain:
                        print("chain colored")
                        chain.name = "CCC"
                        # redchain = False
                        dirty_structures.append(chain)
                        # continue
                    for residue in chain.residues:
                        if redresidue:
                            print("residue colored")
                            residue.name = "DDD"
                            # redresidue = False
                            dirty_structures.append(residue)
                            # continue
                        for bond in residue.bonds:
                            if redbond:
                                bond.kind = _Bond.Kind.CovalentTriple
                                print("bond colored")
                                # redbond = False
                                dirty_structures.append(bond)
                                # continue                            
                        for atom in residue.atoms:
                            if redatom:
                                print("atom colored")
                                atom.name = "EEE"
                                # redatom = False
                                dirty_structures.append(atom)
                                # continue                            
        nanome.util.Logs.debug("XXXXXXXXXXXXXXXXXXXXXXXX")
        nanome.util.Logs.debug(len(dirty_structures))
        self.update_structures_shallow(dirty_structures)

    def on_run(self):
        self.request_workspace(self.on_workspace_received)

    def __init__(self):
        pass

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, ShallowUpdatePlugin, NTS_ADDRESS, NTS_PORT)