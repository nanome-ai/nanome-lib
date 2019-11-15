import nanome
import testing
import os
from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

class PrintWorkspace(FuzzerCommand):
    def __init__(self, fuzzer_info, plugin):
        FuzzerCommand.__init__(self, fuzzer_info, plugin)

    def _get_name(self):
        return "Print Workspace"

    def _rules(self):
        return True

    def _run(self):
        self.plugin.request_workspace(self.receive_workspace)

    def receive_workspace(self, workspace):
        names = ""
        for complex in workspace.complexes:
            names += " [" + complex.name + "]"
        Logs.message(names)
        self.finish()