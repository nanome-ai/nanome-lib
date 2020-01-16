import nanome
from nanome.util import Logs
import sys
import time

# Config

NAME = "Sand Box"
DESCRIPTION = "A plugin that can be edited freely for testing."
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False

# Plugin

class SandBox(nanome.PluginInstance):
    def start(self):
        self.request_presenter_info(self.received)
        self.send_notification(nanome.util.enums.NotificationTypes.message, "A" + "\u0394" + "A")

    def on_presenter_change(self):
        self.request_presenter_info(self.received)

    def received(self, presenter_info):
        Logs.message("Presenter:", presenter_info.account_id, presenter_info.account_name, presenter_info.account_email)

    def on_run(self):
        self.request_workspace(self.y)

    def x(self, workspace):
        for complex in workspace.complexes:
            for bond in complex.bonds:
                for i in range(len(bond._kinds)):
                    bond._kinds[i] = nanome.util.enums.Kind.safe_cast((i % 3) + 1)
            for atom in complex.atoms:
                for i in range(len(atom._positions)):
                    atom._positions[i].x = i
            for molecule in complex.molecules:
                for i in range(len(molecule._names)):
                    molecule._names[i] = str(i) + str(i)
        self.update_workspace(workspace)

    def y(self, workspace):
        for complex in workspace.complexes:
            for bond in complex.bonds:
                bond.kind = nanome.util.enums.Kind.safe_cast(3)
            for atom in complex.atoms:
                pos = atom.position
                temp = pos.x
                pos.x = pos.y
                pos.y = pos.z
                pos.z = temp
            for molecule in complex.molecules:
                molecule.name = "it works jeremie"
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

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SandBox)