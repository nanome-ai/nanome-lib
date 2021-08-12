from nanome.api.structure import molecule
import nanome
import sys
import time

# Config

NAME = "Substructure Test Plugin"
DESCRIPTION = "Simple plugin demonstrating the substructure features."
CATEGORY = "Test"
HAS_ADVANCED_OPTIONS = False

# Plugin

class SubstructuresPlugin(nanome.PluginInstance):
    def start(self):
        print("Start SubstructuresPlugin Plugin")

    def on_run(self):
        print("Run SubstructuresPlugin Plugin")
        self.request_workspace(self.on_workspace_received)

    def on_workspace_received(self, workspace):
        print("workspace received")

        for complex in workspace.complexes:
            molecule = list(complex.molecules)[complex.current_frame]
            molecule.get_proteins(self.on_proteins)
            molecule.get_ligands(self.on_ligands)
            molecule.get_solvents(self.on_solvents)
            molecule.get_substructures(self.on_substructures)
            
    def on_proteins(self, subs):
        print("on_proteins")
        unique = {}
        for sub in subs:
            s = (sub.name, len(list(sub.residues)), sub.structure_type)
            if s in unique:
                unique[s] = unique[s] + 1
            else:
                unique[s] = 0
        for s in unique.keys():
            name, length, type = s
            print (name, length, type, unique[s])

    def on_ligands(self, subs):
        print("on_ligands")
        unique = {}
        for sub in subs:
            s = (sub.name, len(list(sub.residues)), sub.structure_type)
            if s in unique:
                unique[s] = unique[s] + 1
            else:
                unique[s] = 0
        for s in unique.keys():
            name, length, type = s
            print (name, length, type, unique[s])

    def on_solvents(self, subs):
        print("on_solvents")
        unique = {}
        for sub in subs:
            s = (sub.name, len(list(sub.residues)), sub.structure_type)
            if s in unique:
                unique[s] = unique[s] + 1
            else:
                unique[s] = 0
        for s in unique.keys():
            name, length, type = s
            print (name, length, type, unique[s])

    def on_substructures(self, subs):
        print("on_substructures")
        unique = {}
        for sub in subs:
            s = (sub.name, len(list(sub.residues)), sub.structure_type)
            if s in unique:
                unique[s] = unique[s] + 1
            else:
                unique[s] = 0
        for s in unique.keys():
            name, length, type = s
            print (name, length, type, unique[s])

    def __init__(self):
        pass

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SubstructuresPlugin)