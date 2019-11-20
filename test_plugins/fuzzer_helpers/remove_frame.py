import nanome
import testing
import os
from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

class RemoveFrame(FuzzerCommand):
    def __init__(self, fuzzer_info, plugin):
        FuzzerCommand.__init__(self, fuzzer_info, plugin)

    def _get_name(self):
        return "Remove Frame"

    def _rules(self):
        return self.fuzzer_info.complex_count > 0

    def _run(self):
        self.plugin.request_workspace(self.receive_workspace)

    def receive_workspace(self, workspace):
        complexes = workspace.complexes
        r_c = testing.rand_index(complexes)
        complex = workspace.complexes[r_c]
        has_conformer = self.has_conformer(complex)
        if  has_conformer:
            Logs.message("complex " + complex.name + " uses conformer")
            molecule = next(complex.molecules)
            if molecule.conformer_count < 2:
                self.finish()
                return
            r_i = testing.rand_int(0, molecule.conformer_count-1)
            Logs.message("removing conformer " + r_i + "/" + len(molecule.conformer_count))
            molecule.delete_conformer(r_i)
        else:
            Logs.message("complex " + complex.name + " uses frames")
            mols = list(complex.molecules)
            if len(mols) < 2:
                self.finish()
                return
            r_i = testing.rand_index(mols)
            Logs.message("removing frame " + r_i + "/" + len(mols))
            complex.remove_molecule(mols[r_i])
        self.plugin.update_structures_deep([complex], self.finish)

    def has_conformer (self, complex):
        all_mol = list(complex.molecules)
        if len(all_mol) > 1:
            return False
        mol = all_mol[0]
        if mol.conformer_count > 1:
            return True
        #default
        return False