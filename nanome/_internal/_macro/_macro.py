import nanome
import string
import random
from nanome._internal._network._commands._callbacks import _Messages

class _Macro(object):
    #generates a different random identifier for each instance of the plugin lib.
    _plugin_identifier = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(12))

    def __init__(self):
        self._title = ""
        self._logic = ""

    @classmethod
    def _create(cls):
        return cls()

    def _save(self, all_users = False):
        nanome._internal._network._ProcessNetwork._send(_Messages.save_macro, (self, all_users, _Macro._plugin_identifier), False)

    def _run(self, callback = None):
        id = nanome._internal._network._ProcessNetwork._send(_Messages.run_macro, self, callback != None)
        if callback != None:
            nanome._internal._PluginInstance._save_callback(id, callback)

    def _delete(self, all_users = False):
        nanome._internal._network._ProcessNetwork._send(_Messages.delete_macro, (self, all_users, _Macro._plugin_identifier), False)

    @classmethod
    def _stop(cls):
        nanome._internal._network._ProcessNetwork._send(_Messages.stop_macro, None, False)
    
    @classmethod
    def _get_live(cls, callback):
        id = nanome._internal._network._ProcessNetwork._send(_Messages.get_macros, _Macro._plugin_identifier, callback != None)
        nanome._internal._PluginInstance._save_callback(id, callback)