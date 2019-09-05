import sys, multiprocessing, time, importlib

def launch_plugin(class_name, args):
    module_name = "test_plugins." + class_name
    import nanome
    sys.argv = args
    module = importlib.import_module(module_name)
    plugin_class = importlib.import_module(module_name, class_name)
    plugin = nanome.Plugin(module.NAME, module.DESCRIPTION, module.CATEGORY, module.HAS_ADVANCED_OPTIONS)
    plugin.set_plugin_class(plugin_class)
    plugin.run("config", "config", "config")

if __name__ == "__main__":
    class_name = sys.argv[1]
    del sys.argv[1]
    if class_name.lower() == "all":
        class_names = []
        from os.path import dirname, basename, isfile, join
        import glob
        modules = glob.glob(join(dirname(__file__), join("test_plugins", "*.py")))
        class_names = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
        for class_name in class_names:
            x = multiprocessing.Process(target=launch_plugin, args = (class_name, sys.argv))
            x.start()
        while(True):
            time.sleep(1)
    else:
        importlib.import_module("test_plugins." + class_name)