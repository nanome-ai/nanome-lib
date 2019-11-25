import nanome
import testing
import os
from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

class DuplicateFrame(FuzzerCommand):
    def __init__(self, fuzzer_info, plugin):
        FuzzerCommand.__init__(self, fuzzer_info, plugin)

    def _get_name(self):
        return "Duplicate Frame"

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
            r_i = testing.rand_int(0, molecule.conformer_count-1)
            Logs.message("duplicating conformer " + str(r_i) + "/" + str(molecule.conformer_count))
            molecule.copy_conformer(r_i)
        else:
            Logs.message("complex " + complex.name + " uses frames")
            mols = list(complex.molecules)
            r_i = testing.rand_index(mols)
            Logs.message("duplicating frame " + str(r_i) + "/" + str(len(mols)))
            complex.add_molecule(mols[r_i]._deep_copy())
        self.plugin.update_structures_deep([complex], self.finish)