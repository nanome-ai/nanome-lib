import nanome
import testing
import os
from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

test_cifs = os.path.join(os.getcwd(), "testing/test_assets/mmcif")
cif_count = 0
class AddCIF(FuzzerCommand):
    def __init__(self, fuzzer_info, plugin):
        FuzzerCommand.__init__(self, fuzzer_info, plugin)

    def _get_name(self):
        return "Add CIF"

    def _rules(self):
        return self.fuzzer_info.complex_count < 10

    def _run(self):
        cifs = os.listdir(test_cifs)
        r_i = testing.rand_index(cifs)
        rand_cif = cifs[r_i]
        Logs.message("loading cif", rand_cif)
        full_path = os.path.join(test_cifs, rand_cif)
        new_complex = nanome.structure.Complex.io.from_mmcif(path=full_path)
        global cif_count
        new_complex.name = "CIF" + str(cif_count)
        cif_count+=1
        self.fuzzer_info.complex_count += 1
        self.plugin.update_structures_deep([new_complex], self.finish)