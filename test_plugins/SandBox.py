import nanome
from nanome.util import Logs
import sys
import time
class SandBox(nanome.PluginInstance):
    def start(self):
        print("Started")


    def on_run(self):
        self.request_complex_list(self.on_complex_list_received)

    def on_complex_list_received(self, complexes):
        Logs.debug("complex received: ", complexes)
        ids = []
        for complex in complexes:
            ids.append(complex._index)
            ids.append(7)
        self.request_complexes(ids, self.on_complexes_received)

    def on_complexes_received(self, complexes):
        for complex in complexes:
            if (complex is None):
                Logs.debug("None received")
            else:
                Logs.debug(complex.molecules)


    def __init__(self):
        pass

if __name__ == "__main__":
    plugin = nanome.Plugin("Sand Box", "A plugin that can be edited freely for testing.", "Test", False)
    plugin.set_plugin_class(SandBox)
    plugin.run('127.0.0.1', 8888)