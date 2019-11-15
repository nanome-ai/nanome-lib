import nanome
import testing
import os
from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

test_sdfs = os.path.join(os.getcwd(), "testing/test_assets/sdf")
sdf_count = 0
class AddSDF(FuzzerCommand):
    def __init__(self, fuzzer_info, plugin):
        FuzzerCommand.__init__(self, fuzzer_info, plugin)

    def _get_name(self):
        return "Add SDF"

    def _rules(self):
        return self.fuzzer_info.complex_count < 10

    def _run(self):
        sdfs = os.listdir(test_sdfs)
        r_i = testing.rand_index(sdfs)
        rand_sdf = sdfs[r_i]
        Logs.message("loading sdf", rand_sdf)
        full_path = os.path.join(test_sdfs, rand_sdf)
        new_complex = nanome.structure.Complex.io.from_sdf(path=full_path)
        global sdf_count
        new_complex.name = "SDF" + str(sdf_count)
        sdf_count+=1
        self.fuzzer_info.complex_count += 1
        self.plugin.update_structures_deep([new_complex], self.finish)