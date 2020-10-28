import os
import nanome
from nanome.api import structure as struct
from nanome.util import enums
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
        self.apply_color_scheme(enums.ColorScheme.BFactor, enums.Mode.All, False)

def __init__(self):
        pass


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SandBox)
