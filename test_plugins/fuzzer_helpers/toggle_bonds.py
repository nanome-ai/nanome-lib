import nanome
import testing
import os
from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

class ToggleBonds(FuzzerCommand):
    def __init__(self, fuzzer_info, plugin):
        FuzzerCommand.__init__(self, fuzzer_info, plugin)

    def _get_name(self):
        return "Toggle Bonds"

    def _rules(self):
        return self.fuzzer_info.complex_count > 0

    def _run(self):
        self.get_random_complex(self.receive_complex)

    def receive_complex(self, complex):
        Logs.message("toggling bonds on complex: " + complex.name)
        has_bonds = self.has_bonds(complex)
        if has_bonds:
            Logs.message("removing bonds")
            all_bonds = list(complex.bonds)
            for bond in all_bonds:
                bond.residue.remove_bond(bond)
                bond.atom1 = None
                bond.atom2 = None
            self.plugin.update_structures_deep([complex], self.finish)
        else:
            Logs.message("adding bonds")
            self.plugin.add_bonds([complex], self.added_bonds)

    def added_bonds(self, complexes):
        self.plugin.update_structures_deep(complexes, self.finish)

    def has_bonds(self, complex):
        try:
            next(complex.bonds)
            return True
        except StopIteration:
            return False