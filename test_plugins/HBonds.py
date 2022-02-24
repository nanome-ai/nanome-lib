import nanome
from nanome.util import Logs
from nanome.api.structure import Workspace
import sys
import time

# Config

NAME = "Hydrogen Bonds"
DESCRIPTION = "Computes HBonds using nanome default behavior."
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False

# Plugin


class HBonds(nanome.PluginInstance):
    def start(self):
        pass

    def on_run(self):
        Workspace.client.compute_hbonds(self.print_callback)

    def print_callback(self):
        Logs.message("hbonds complete")


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, HBonds)
