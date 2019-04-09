import nanome
import sys
import os

from nanome.util import Logs
from nanome.api.structure import Complex, Workspace


class LoadFile(nanome.PluginInstance):
    filename = "\\mmcif\\tebgit.cif"
    test_assets = os.getcwd() + ("\\testing\\test_assets")

    def start(self):
        print("Start Load File")

    def on_run(self):
        filename = LoadFile.filename
        test_assets = LoadFile.test_assets
        ext = filename.split(".")[-1]
        if (ext == "pdb"):
            input_dir = (test_assets + filename)
            Logs.debug("reading " + input_dir)
            complex1 = Complex.io.from_pdb(input_dir)
        elif (ext == "cif"):
            input_dir = (test_assets + filename)
            Logs.debug("reading " + input_dir)
            complex1 = Complex.io.from_mmcif(input_dir)
        elif (ext == "sdf"):
            input_dir = (test_assets + filename)
            Logs.debug("reading " + input_dir)
            complex1 = Complex.io.from_sdf(input_dir)
        else:
            raise Exception("invalid file: " + filename)
        workspace = Workspace()
        workspace.complexes = [complex1]
        self.update_workspace(workspace)

    def __init__(self):
        pass

if __name__ == "__main__":
    plugin = nanome.Plugin("Load File", "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities", "Test", False)
    plugin.set_plugin_class(LoadFile)
    plugin.run('127.0.0.1', 8888)