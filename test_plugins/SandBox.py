import nanome
from nanome.util import Logs
import sys
import time
class SandBox(nanome.PluginInstance):
    def start(self):
        print("Started")


    def on_run(self):
        self.request_complex_list(self.on_complex_list_received)

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

if __name__ == "__main__":
    plugin = nanome.Plugin("Sand Box", "A plugin that can be edited freely for testing.", "Test", False)
    plugin.set_plugin_class(SandBox)
    plugin.run('127.0.0.1', 8888)