import nanome
import testing
import os
from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

class RemoveComplex(FuzzerCommand):
    def __init__(self, fuzzer_info, plugin):
        FuzzerCommand.__init__(self, fuzzer_info, plugin)

    def _get_name(self):
        return "Remove Complex"

    def _rules(self):
        return self.fuzzer_info.complex_count > 0

    def _run(self):
        self.plugin.request_workspace(self.receive_workspace)

    def receive_workspace(self, workspace):
        complexes = workspace.complexes
        r_c = testing.rand_index(complexes)
        Logs.message("removing complex: " + workspace.complexes[r_c].name)
        del workspace.complexes[r_c]
        self.plugin.update_workspace(workspace)
        self.fuzzer_info.complex_count -= 1
        self.finish()