import nanome
import string
import random
from nanome._internal.network import PluginNetwork
from nanome._internal.enums import Messages


class Macro:

    # generates a different random identifier for each instance of the plugin lib.
    _plugin_identifier = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(12))

    def __init__(self, title="", logic=""):
        self.title = title
        self.logic = logic

    @classmethod
    def get_plugin_identifier(cls):
        return cls._plugin_identifier

    @classmethod
    def set_plugin_identifier(cls, value):
        cls._plugin_identifier = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def logic(self):
        return self._logic

    @logic.setter
    def logic(self, value):
        self._logic = value

    def save(self, all_users=False):
        self._save(all_users)

    def run(self, callback=None):
        return self._run(callback)

    def delete(self, all_users=False):
        self._delete(all_users)

    @classmethod
    def stop(cls):
        cls._stop()

    @classmethod
    def get_live(cls, callback=None):
        return cls._get_live(callback)

    def _save(self, all_users=False):
        PluginNetwork.send(Messages.save_macro, (self, all_users, self._plugin_identifier), False)

    def _run(self, callback=None):
        expects_response = callback is not None or nanome.PluginInstance._instance.is_async
        id = PluginNetwork.send(Messages.run_macro, self, expects_response)
        return nanome.PluginInstance._save_callback(id, callback)

    def _delete(self, all_users=False):
        PluginNetwork.send(Messages.delete_macro, (self, all_users, self._plugin_identifier), False)

    @classmethod
    def _stop(cls):
        PluginNetwork.send(Messages.stop_macro, None, False)

    @classmethod
    def _get_live(cls, callback=None):
        expects_response = callback is not None or nanome.PluginInstance._instance.is_async
        id = PluginNetwork.send(Messages.get_macros, cls._plugin_identifier, expects_response)
        return nanome.PluginInstance._save_callback(id, callback)
