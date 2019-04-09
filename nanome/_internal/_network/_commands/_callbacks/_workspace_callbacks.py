from nanome.util.logs import Logs
from nanome._internal._ui import _Menu

def _receive_workspace(network, arg, request_id):
    network._call(request_id, arg)

def _complex_added(network, arg, request_id):
    network.on_complex_added()

def _complex_removed(network, arg, request_id):
    network.on_complex_removed()