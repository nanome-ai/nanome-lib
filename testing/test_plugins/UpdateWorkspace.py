import nanome
import sys
import time

# Config

NAME = "Update Workspace"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False

# Plugin


class UpdateWorkspace(nanome.PluginInstance):
    def start(self):
        print("Start UpdateWorkspace Plugin")

    def on_workspace_received(self, workspace):
        print("running")
        atom_count = 0
        bond_count = 0
        for complex in workspace.complexes:
            for molecule in complex.molecules:
                for chain in molecule.chains:
                    for residue in chain.residues:
                        for bond in residue.bonds:
                            bond_count += 1
                        for atom in residue.atoms:
                            atom.position.x = -atom.position.x
                            atom.surface_rendering = True
                            atom.surface_color = nanome.util.Color.Red()
                            atom_count += 1

        print("bonds:", bond_count)
        print("flipped", atom_count, "atoms")
        self.update_workspace(workspace)

    def on_run(self):
        self.request_workspace(self.on_workspace_received)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, UpdateWorkspace)
