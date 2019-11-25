import nanome
import testing
import os
from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

class ChangeFrame(FuzzerCommand):
    def __init__(self, fuzzer_info, plugin):
        FuzzerCommand.__init__(self, fuzzer_info, plugin)

    def _get_name(self):
        return "Change Frame"

    def _rules(self):
        return self.fuzzer_info.complex_count > 0

    def _run(self):
        self.get_random_complex(self.receive_complex)

    def receive_complex(self, complex):
        has_conformer = self.has_conformer(complex)
        if  has_conformer:
            Logs.message("complex " + complex.name + " uses conformer")
            molecule = next(complex.molecules)
            r_i = testing.rand_int(0, molecule.conformer_count-1)
            Logs.message("changing to conformer " + str(r_i) + "/" + str(molecule.conformer_count))
            molecule.set_current_conformer(r_i)
        else:
            Logs.message("complex " + complex.name + " uses frames")
            mols = list(complex.molecules)
            r_i = testing.rand_index(mols)
            Logs.message("changing to frame " + str(r_i) + "/" + str(len(mols)))
            complex.set_current_frame(r_i)
        complex.set_surface_needs_redraw()
        self.plugin.update_structures_deep([complex], self.finish)