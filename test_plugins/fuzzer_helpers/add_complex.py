from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

class AddComplex(FuzzerCommand):
    def __init__(self, fuzzer_info):
        FuzzerCommand.__init__(self, fuzzer_info)

    def _get_name(self):
        return "Add Complex"

    def _rules(self):
        return self.fuzzer_info.complex_count < 10

    def _run(self):
        Logs.message("added complex")
        self.finish()