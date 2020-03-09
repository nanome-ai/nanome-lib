from nanome.util import Logs

class Integration():
    def __init__(self):
        self.on_add_hydrogen = None
        self.on_remove_hydrogen = None

    @classmethod
    def _call(cls, name, request):
        callback = getattr(cls, name, None)
        if callback == None:
            Logs.warning("Integration", name, "called without being set by the plugin")
            return
        callback(request)
