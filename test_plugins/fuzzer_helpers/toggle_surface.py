import nanome
import testing
import os
from .fuzzer_command import FuzzerCommand
from nanome.util import Logs

class ToggleSurface(FuzzerCommand):
    def __init__(self, fuzzer_info, plugin):
        FuzzerCommand.__init__(self, fuzzer_info, plugin)

    def _get_name(self):
        return "Toggle Surface"

    def _rules(self):
        return self.fuzzer_info.complex_count > 0

    def _run(self):
        self.get_random_complex(self.receive_complex)

    def receive_complex(self, complex):
        Logs.message("toggling surface on complex: " + complex.name)
        for atom in complex.atoms:
            atom.surface_rendering = not atom.surface_rendering
        complex.set_surface_needs_redraw()
        self.plugin.update_structures_deep([complex], self.finish)