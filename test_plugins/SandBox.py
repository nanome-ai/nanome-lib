import os
import nanome
from nanome.api import structure as struct
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
        pass

    def on_run(self):
        self.request_workspace(self.work)

    def work(self, workspace):
        targetComplex = workspace._complexes[0]
        other = workspace._complexes[1:]
        struct.Complex.align_origins(targetComplex, *other)
        self.update_workspace(workspace)

def __init__(self):
        pass


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SandBox)
