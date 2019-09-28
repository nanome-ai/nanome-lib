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

    def create_topology_and_positions(self, complex_list, topology, positions):
        for complex in complex_list:
            conformers_enabled = self.is_new_system(complex)
            molecule = complex.molecules[complex.current_frame]
            for chain in molecule.chains:
                if conformers_enabled and not self.structure_exists(chain):
                    continue
                sim_chain = topology.addChain()
                for residue in chain.residues:
                    if conformers_enabled and not self.structure_exists(residue):
                        continue
                    sim_residue = topology.addResidue(residue.name, sim_chain)
                    atomReplacements = PDBFile._atomNameReplacements.get(residue.name, {})
                    for atom in residue.atoms:
                        if conformers_enabled and not atom.exists:
                            continue
                        symbol = MDSimulationProcess.get_atom_symbol(atom.name, len(residue._atoms))
                        atom_name = atom.name
                        if atom_name in atomReplacements:
                            atom_name = atomReplacements[atom_name]
                        sim_atom = topology.addAtom(atom_name, symbol, sim_residue)
                        position = atom.position
                        positions.append(Vec3(position.x * 0.1 * nanometer,  position.y * 0.1 * nanometer, position.z * 0.1 * nanometer))
        return (topology, positions)


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
    elif len(class_names) > 1:
        import glob
        modules = glob.glob(join(dirname(__file__), join("test_plugins", "*.py")))
        class_names = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
        for class_name in class_names:
            x = multiprocessing.Process(target=launch_plugin, args = (class_name, sys.argv))
            x.start()
        while(True):
            time.sleep(1)
    else:
        import nanome
        nanome.util.Logs.error("No plugin found")