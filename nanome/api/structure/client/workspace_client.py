import nanome
from nanome._internal._network._commands._callbacks import _Messages
from nanome._internal._addon import _Addon

class WorkspaceClient(_Addon):
    def __init__(self, base_object=None):
        _Addon.__init__(self, base_object)

    @classmethod
    def compute_hbonds(cls, callback):
        id = nanome._internal._network._ProcessNetwork._send(_Messages.compute_hbonds, None, callback != None)
        nanome._internal._PluginInstance._save_callback(id, callback)

