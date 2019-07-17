import nanome
from nanome.util import Logs
import sys
import time

# Config

NAME = "Sand Box"
DESCRIPTION = "A plugin that can be edited freely for testing."
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False
NTS_ADDRESS = '127.0.0.1'
NTS_PORT = 8888

# Plugin

class SandBox(nanome.PluginInstance):
    def start(self):
        print("Started")


    def on_run(self):
        self.request_workspace(self.combine_frames)
        # self.request_complex_list(self.on_complex_list_received)

    def combine_frames(self, workspace):
        frames = []
        for complex in workspace.complexes:
            for molecule in complex.molecules:
                molecule.index = -1
                frames.append(molecule)
            for chain in complex.chains:
                chain.index = -1
            for residue in complex.residues:
                residue.index = -1
            for atom in complex.atoms:
                atom.index = -1
            for bond in complex.bonds:
                bond.index = -1

        workspace.complexes[0]._molecules = frames
        workspace.complexes = [workspace.complexes[0]]
        self.update_workspace(workspace)

    def x(self, workspace):
        super_complex = None
        super_residue = None
        for complex in workspace.complexes:
            super_complex = complex
            for residue in complex.residues:
                super_residue = residue
                break
            break
        for complex in workspace.complexes:
            for residue in complex.residues:
                for atom in residue.atoms:
                    if not super_residue is residue:
                        atom.position = atom.position + complex.position - super_complex.position
                        super_residue.add_atom(atom)
                for bond in residue.bonds:
                    if not super_residue is residue:
                        super_residue.add_bond(bond)

        workspace.complexes = [super_complex]
        self.update_workspace(workspace)

    def on_complex_list_received(self, complexes):
        Logs.debug("complex received: ", complexes)
        ids = []
        Logs.debug("Requested complex list")
        for complex in complexes:
            Logs.debug("selected: " + str(complex.get_selected()))
            ids.append(complex._index)
            ids.append(7)
        self.request_complexes(ids, self.on_complexes_received)

    def on_complexes_received(self, complexes):
        Logs.debug("Requested complexes")
        for complex in complexes:
            if (complex is None):
                Logs.debug("None received")
            else:
                complex.locked = True
                self.label_all(complex)
                self.update_structures_deep([complex])
                

    def label_all(self, complex):
        all_labeled = True
        all_text = True
        for residue in complex.residues:
            all_labeled = all_labeled and residue.labeled
            all_text = all_text and residue.label_text == "RESIDUE"
            residue.labeled = True
            residue.label_text = "RESIDUE"
            for atom in residue.atoms:
                all_labeled = all_labeled and atom.labeled
                all_text = all_text and atom.label_text == "ATOM"
                atom.labeled = True
                atom.label_text = "ATOM"
        Logs.debug("labeled:", all_labeled)
        Logs.debug("correct text:", all_text)

    def __init__(self):
        pass

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SandBox, NTS_ADDRESS, NTS_PORT)