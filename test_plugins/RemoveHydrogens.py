import nanome
from nanome.util import Logs

class RemoveHydrogens(nanome.PluginInstance):
    def __init__(self):
        pass

    # When user clicks on "Activate"
    def start(self):
        Logs.debug("Connected to a new session!")
    
    @staticmethod
    def _should_be_removed(atom):
        if atom.rendering.selected == False:
            return False
        if atom.molecular.symbol != 'H':
            return False
        return True

    # When user clicks on "Run"
    def on_run(self):
        self.request_workspace(self.on_workspace_received) # Request the entire workspace, in "deep" mode

     # When we receive the entire workspace from Nanome
    def on_workspace_received(self, workspace):
        for complex in workspace.complexes:
            count = 0
            for residue in complex.residues:
                for i in range(len(residue._atoms) - 1, -1, -1):
                    if RemoveHydrogens._should_be_removed(residue._atoms[i]): # If this atom is an H, delete it
                        count += 1
                        del residue._atoms[i]
            Logs.debug(count, "hydrogens removed for", complex.molecular.name)
        self.update_workspace(workspace) # Update Nanome workspace, in "deep" mode
        
if __name__ == "__main__":
    # Creates the server, register RemoveHydrogens as the class to instantiate, and start listening for connections
    plugin = nanome.Plugin("Remove Hydrogens", "Remove hydrogens in all selected atoms", "Simple Actions", False)
    plugin.set_plugin_class(RemoveHydrogens)
    plugin.run('127.0.0.1', 8888)