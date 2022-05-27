import nanome
from nanome.util import Logs

NAME = "Atom Typing Test"
DESCRIPTION = "Tests generic atom type API"
CATEGORY = "Tests"
HAS_ADVANCED_OPTIONS = False


class AtomTypingTest(nanome.PluginInstance):
    def start(self):
        pass

    def on_run(self):
        self.request_workspace(self.on_receive_workspace)

    def on_receive_workspace(self, workspace: nanome.structure.Workspace):
        complex: nanome.structure.Complex
        for complex in workspace.complexes:
            atom: nanome.structure.Atom
            for atom in complex.atoms:
                print(atom._atom_type)
                atom._atom_type["Test"] = "TestAtomType"
        self.update_workspace(workspace)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY,
                    HAS_ADVANCED_OPTIONS, AtomTypingTest)
