import nanome
import sys
import os
import testing.utilities

from nanome.util import Logs
from nanome.api.structure import Complex, Workspace

# Config

NAME = "EM Plugin"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Test"
HAS_ADVANCED_OPTIONS = False
NTS_ADDRESS = '127.0.0.1'
NTS_PORT = 8888

# Plugin

class EMPlugin(nanome.PluginInstance):
    def start(self):
        print("Start Load File")

    def on_run(self):
        path = testing.utilities.get_test_assets() + "volumetric\\cryo_em\\0170.map.gz"
        self.upload_cryo_em(path, self.on_em_uploaded)
    
    def on_advanced_settings(self):
        Logs.debug("adv pressed")

    def on_em_uploaded(self):
        pass

    def __init__(self):
        self.zoom = True
        pass

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, EMPlugin, NTS_ADDRESS, NTS_PORT)