import nanome
from nanome._internal._addon import _Addon
from nanome._internal._network import PluginNetwork
from nanome._internal._network._commands._callbacks import _Messages


class WorkspaceClient(_Addon):
    def __init__(self, base_object=None):
        _Addon.__init__(self, base_object)

    @classmethod
    def compute_hbonds(cls, callback=None):
        expects_response = callback is not None or nanome.PluginInstance._instance.is_async
        id = PluginNetwork._send(_Messages.compute_hbonds, None, expects_response)
        return nanome.PluginInstance._save_callback(id, callback)
