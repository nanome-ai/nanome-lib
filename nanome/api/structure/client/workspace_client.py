import nanome
from nanome._internal.addon import _Addon
from nanome._internal.network import PluginNetwork
from nanome._internal.enums import Messages


class WorkspaceClient(_Addon):
    def __init__(self, base_object=None):
        _Addon.__init__(self, base_object)

    @classmethod
    def compute_hbonds(cls, callback=None):
        expects_response = callback is not None or nanome.PluginInstance._instance.is_async
        id = PluginNetwork.send(Messages.compute_hbonds, None, expects_response)
        return nanome.PluginInstance._save_callback(id, callback)
