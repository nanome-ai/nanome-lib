import nanome
import testing
import os
from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

test_pdbs = os.path.join(os.getcwd(), "testing/test_assets/pdb")
pdb_count = 0
class AddPDB(FuzzerCommand):
    def __init__(self, fuzzer_info, plugin):
        FuzzerCommand.__init__(self, fuzzer_info, plugin)

    def _get_name(self):
        return "Add PDB"

    def _rules(self):
        return self.fuzzer_info.complex_count < 10

    def _run(self):
        pdbs = os.listdir(test_pdbs)
        r_i = testing.rand_index(pdbs)
        rand_pdb = pdbs[r_i]
        Logs.message("loading pdb", rand_pdb)
        full_path = os.path.join(test_pdbs, rand_pdb)
        new_complex = nanome.structure.Complex.io.from_pdb(path=full_path)
        global pdb_count
        new_complex.name = "PDB" + str(pdb_count)
        pdb_count+=1
        self.fuzzer_info.complex_count += 1
        self.plugin.update_structures_deep([new_complex], self.finish)