import nanome
import sys
import os

from nanome.util import Logs
from nanome.api.structure import Complex, Workspace

# Config

NAME = "Load File"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Test"
HAS_ADVANCED_OPTIONS = False

# Plugin


class LoadFile(nanome.PluginInstance):
    filename = "/mmcif/tebgit.cif"
    test_assets = os.getcwd() + ("/testing/test_assets")

    def start(self):
        print("Start Load File")

    def on_run(self):
        def done(res):
            for r in res:
                Logs.debug("Success", r.success)

        self.send_files_to_load([LoadFile.test_assets + LoadFile.filename], done)
        # filename = LoadFile.filename
        # test_assets = LoadFile.test_assets
        # ext = filename.split(".")[-1]
        # if (ext == "pdb"):
        #     input_dir = (test_assets + filename)
        #     Logs.debug("reading " + input_dir)
        #     complex1 = Complex.io.from_pdb(file=input_dir)
        # elif (ext == "cif"):
        #     input_dir = (test_assets + filename)
        #     Logs.debug("reading " + input_dir)
        #     complex1 = Complex.io.from_mmcif(file=input_dir)
        # elif (ext == "sdf"):
        #     input_dir = (test_assets + filename)
        #     Logs.debug("reading " + input_dir)
        #     complex1 = Complex.io.from_sdf(file=input_dir)
        # else:
        #     raise Exception("invalid file: " + filename)
        # workspace = Workspace()
        # workspace.complexes = [complex1]
        # self.update_workspace(workspace)

    def on_advanced_settings(self):
        Logs.debug("adv pressed")
        self.request_workspace(self.on_workspace_received)

    def on_workspace_received(self, workspace):
        Logs.debug("workspace received")
        atoms = []
        for complex in workspace.complexes:
            for atom in complex.atoms:
                if atom.selected:
                    atoms.append(atom)
        if self.zoom:
            self.zoom_on_structures(atoms, lambda: print("Zoomed"))
            self.zoom = False
        else:
            self.center_on_structures(atoms, lambda: print("Centered"))
            self.zoom = True

    def __init__(self):
        self.zoom = True
        pass


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, LoadFile)
