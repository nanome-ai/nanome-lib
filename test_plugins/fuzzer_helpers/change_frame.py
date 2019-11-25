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
        self.if_has_conformer(complex,
                              lambda complex : self.get_random_conformer(complex, self.change_conformer),
                              lambda complex : self.get_random_molecule(complex, self.change_frame))
    def change_conformer(self, molecule, index):
        Logs.message("complex " + molecule.complex.name + " uses conformer")
        Logs.message("changing to conformer " + str(index) + "/" + str(molecule.conformer_count))
        molecule.set_current_conformer(index)
        self.re_upload(molecule.complex)

    def change_frame(self, complex, index):
        mols = list(complex.molecules)
        Logs.message("complex " + complex.name + " uses frames")
        Logs.message("changing to frame " + str(index) + "/" + str(len(mols)))
        complex.set_current_frame(index)
        self.re_upload(complex)

    def re_upload(self, complex):
        complex.set_surface_needs_redraw()
        self.update_structures(complex, self.finish)
