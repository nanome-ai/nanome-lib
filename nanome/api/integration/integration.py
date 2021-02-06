from nanome.util import Logs

class Integration():
    def __init__(self):
        self.hydrogen_add = None
        self.hydrogen_remove = None
        self.structure_prep = None
        self.calculate_esp = None
        self.minimization_start = None
        self.minimization_stop = None
        self.export_file = None
        self.export_locations = None
        self.generate_molecule_image = None
        self.import_file = None

    def _call(self, name, request):
        callback = getattr(self, name, None)
        if callback == None:
            Logs.warning("Integration", name, "called without being set by the plugin")
            return
        callback(request)
