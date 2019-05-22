import nanome
import sys
import os
import testing.utilities

from nanome.util import Logs
from nanome.api.structure import Complex, Workspace

class EMPlugin(nanome.PluginInstance):
    def start(self):
        print("Start Load File")

    def on_run(self):
        path = testing.utilities.get_test_assets() + "volumetric\\cryo_em\\0170.map.gz"
        self.upload_cyro_em(path, self.on_em_uploaded)
    
    def on_advanced_settings(self):
        Logs.debug("adv pressed")

    def on_em_uploaded(self):
        pass

    def __init__(self):
        self.zoom = True
        pass

if __name__ == "__main__":
    plugin = nanome.Plugin("EM Plugin", "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities", "Test", True)
    plugin.set_plugin_class(EMPlugin)
    plugin.run('127.0.0.1', 8888)