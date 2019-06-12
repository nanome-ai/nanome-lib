import nanome
from timeit import default_timer as timer

import sys, inspect
import test_plugins
if __name__ == "__main__":
    class_name = sys.argv[1]
    module_name = "test_plugins." + class_name
    del sys.argv[1]
    if module_name not in sys.modules:
        raise Exception("No module: " + module_name)
    clsmembers = inspect.getmembers(sys.modules[module_name], inspect.isclass)
    plugin_class = None
    for clsmember in clsmembers:
        if (clsmember[0] == class_name):
            plugin_class = clsmember[1]
            break
    if plugin_class == None:
        raise "No class " + class_name + " in module " + module_name
    plugin = nanome.Plugin(class_name, "Plugin is being run using the tester plugin.", "Test", True)
    plugin.set_plugin_class(plugin_class)
    plugin.run()