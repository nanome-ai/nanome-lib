import nanome
import string
import random
from nanome._internal.network import PluginNetwork
from nanome._internal.enums import Messages


class _Macro(object):
    # generates a different random identifier for each instance of the plugin lib.
    _plugin_identifier = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(12))

    def __init__(self):
        self._title = ""
        self._logic = ""

    @classmethod
    def _create(cls):
        return cls()

    def _save(self, all_users=False):
        PluginNetwork.send(Messages.save_macro, (self, all_users, _Macro._plugin_identifier), False)

    def _run(self, callback=None):
        expects_response = callback is not None or nanome.PluginInstance._instance.is_async
        id = PluginNetwork.send(Messages.run_macro, self, expects_response)
        return nanome.PluginInstance._save_callback(id, callback)

    def _delete(self, all_users=False):
        PluginNetwork.send(Messages.delete_macro, (self, all_users, _Macro._plugin_identifier), False)

    @classmethod
    def _stop(cls):
        PluginNetwork.send(Messages.stop_macro, None, False)

    @classmethod
    def _get_live(cls, callback=None):
        expects_response = callback is not None or nanome.PluginInstance._instance.is_async
        id = PluginNetwork.send(Messages.get_macros, _Macro._plugin_identifier, expects_response)
        return nanome.PluginInstance._save_callback(id, callback)