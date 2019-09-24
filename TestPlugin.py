import sys, multiprocessing, time, importlib, inspect
from os.path import dirname, basename, isfile, join
import glob
# Usage:
# To run a test plugin type "Python TestPlugin.py <plugin name> <args>"
# To run all the test plugins type "Python TestPlugin.py all <args>"
# Example:
# Python TestPlugin.py SandBox -v

def get_class_names():
    modules = glob.glob(join(dirname(__file__), join("test_plugins", "*.py")))
    plugin_modules = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
    if sys.argv[1].lower() == "all":
        del sys.argv[1]
        return plugin_modules
    else:
        class_names = []
        while len(sys.argv) > 1 and sys.argv[1] in plugin_modules:
            class_names.append(sys.argv[1])
            del sys.argv[1]
        return class_names

def launch_plugin(class_name, args):
    module_name = "test_plugins." + class_name
    import nanome
    sys.argv = args
    module = importlib.import_module(module_name)
    plugin = nanome.Plugin(module.NAME, module.DESCRIPTION, module.CATEGORY, module.HAS_ADVANCED_OPTIONS)
    clsmembers = inspect.getmembers(module, inspect.isclass)
    class_target = None
    for clsmember in clsmembers:
        if class_name == clsmember[0]:
            class_target = clsmember[1]
            break
    if class_target == None:
        nanome.util.Logs.error ("Plugin must have the same name as the containing file")
    plugin.set_plugin_class(class_target)
    plugin.run("config", "config", "config")

if __name__ == "__main__":
    class_names = get_class_names()
    if len(class_names) == 1:
        importlib.import_module("test_plugins." + class_names[0])
    else:
        import glob
        modules = glob.glob(join(dirname(__file__), join("test_plugins", "*.py")))
        class_names = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
        for class_name in class_names:
            x = multiprocessing.Process(target=launch_plugin, args = (class_name, sys.argv))
            x.start()
        while(True):
            time.sleep(1)