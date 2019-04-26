import nanome
from timeit import default_timer as timer


class TestPlugin(nanome.PluginInstance):
    def __init__(self):
        self._state = 0

    def update(self):
        end = timer()
        if end - self._start_timer >= 3:
            if self._state == 0:
                self.set_plugin_list_button(nanome.PluginInstance.PluginListButtonType.run, "Nope", False)
                self.set_plugin_list_button(nanome.PluginInstance.PluginListButtonType.advanced_settings, "Nope", False)
            elif self._state == 1:
                self.set_plugin_list_button(nanome.PluginInstance.PluginListButtonType.run, None, True)
                self.set_plugin_list_button(nanome.PluginInstance.PluginListButtonType.advanced_settings, None, True)
            else:
                self.set_plugin_list_button(nanome.PluginInstance.PluginListButtonType.run, "Run", True)
                self.set_plugin_list_button(nanome.PluginInstance.PluginListButtonType.advanced_settings, "Advanced Settings", True)
            self._state = (self._state + 1) % 3
            self._start_timer = timer()

    def start(self):
        # Access the API to add a button on modify menu, name Split, section Editing, and sending event MenuButtonClicked
        nanome.util.Logs.debug("Start TestPlugin")
        self._start_timer = timer()

import sys, inspect
import test_plugins
if __name__ == "__main__":
    plugin_name = "test_plugins." + sys.argv[1]
    del sys.argv[1]
    clsmembers = inspect.getmembers(sys.modules[plugin_name], inspect.isclass)
    plugin_class = clsmembers[0][0]
    plugin = nanome.Plugin("Testing Plugin", "Plugin is being run using the tester plugin.", "Test", True)
    plugin.set_plugin_class(plugin_class)
    plugin.run('127.0.0.1', 8888)