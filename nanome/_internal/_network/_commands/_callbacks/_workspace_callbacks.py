from nanome.util.logs import Logs
from nanome._internal._ui import _Menu

def _complex_added(network, arg, request_id):
    network.on_complex_added()

def _complex_removed(network, arg, request_id):
    network.on_complex_removed()