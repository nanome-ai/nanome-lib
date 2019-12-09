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
        self.get_random_complex(self.receive_complex)

    def receive_complex(self, complex):
        self.if_has_conformer(complex,
                              lambda complex : self.get_random_conformer(complex, self.remove_conformer),
                              lambda complex : self.get_random_molecule(complex, self.remove_frame))

    def remove_conformer(self, molecule, index):
        Logs.message("complex " + molecule.complex.name + " uses conformer")
        Logs.message("removing conformer " + str(index) + "/" + str(molecule.conformer_count))
        if (molecule.conformer_count == 1):
            Logs.message("Too few conformers. Aborting")
            self.finish()
            return
        molecule.delete_conformer(index)
        self.re_upload(molecule.complex)

    def remove_frame(self, complex, index):
        mols = list(complex.molecules)
        num_mols = len(mols)
        if (num_mols == 1):
            Logs.message("Too few frames. Aborting")
            self.finish()
            return
        Logs.message("complex " + complex.name + " uses frames")
        Logs.message("removing frame " + str(index) + "/" + str(num_mols))
        complex.remove_molecule(mols[index])
        self.re_upload(complex)

    def re_upload(self, complex):
        complex.set_surface_needs_redraw()
        self.update_structures(complex, self.finish)