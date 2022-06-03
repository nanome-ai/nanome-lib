import nanome
from nanome.util import Logs

# Config

NAME = "Remove Hydrogens"
DESCRIPTION = "Remove hydrogens in all selected atoms"
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False

# Plugin


class RemoveHydrogens(nanome.PluginInstance):
    # When user clicks on "Activate"
    def start(self):
        Logs.message("Connected to a new session!")  # Displays a message in the console

    @staticmethod
    def _should_be_removed(atom):
        if atom.selected == False:
            return False
        if atom.symbol != 'H':
            return False
        return True

    # When user clicks on "Run"
    def on_run(self):
        self.request_workspace(self.on_workspace_received)  # Request the entire workspace, in "deep" mode

    # When we receive the entire workspace from Nanome
    def on_workspace_received(self, workspace):
        for complex in workspace.complexes:
            count = 0
            for residue in complex.residues:

                # First, find all atoms to remove
                atoms_to_remove = []
                for atom in residue.atoms:
                    # If this atom is an H and is selected, delete it
                    if RemoveHydrogens._should_be_removed(atom):
                        atoms_to_remove.append(atom)

                # Then, remove these atoms
                for atom in atoms_to_remove:
                    residue.remove_atom(atom)
                count += len(atoms_to_remove)

            Logs.debug(count, "hydrogens removed from", complex.molecular.name)  # Displays a message in the console only if plugin started in verbose mode

        self.update_workspace(workspace)  # Update Nanome workspace, in "deep" mode


# Setup plugin information, register RemoveHydrogens as the class to instantiate, and connect to the server
nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, RemoveHydrogens)
