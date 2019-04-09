from nanome.util import Logs
from nanome._internal._network import _ProcessNetwork, _Packet
from nanome._internal._network._commands._callbacks import _Messages

import traceback
import sys

__metaclass__ = type
class _PluginInstance(object):
    __callbacks = dict()

    def _call(self, id, *args):
        callbacks = _PluginInstance.__callbacks
        callbacks[id](*args)
        del callbacks[id]

    def _run(self):
        try:
            self.start()
            while self._network._receive():
                self.update()
        except KeyboardInterrupt:
            return
        except:
            Logs.error(traceback.format_exc())
            self._network._close()
            return
        
    def __init__(self, session_id, pipe, serializer, plugin_id, version_table, original_version_table):
        self._network = _ProcessNetwork(self, session_id, pipe, serializer, plugin_id, version_table)
        Logs.debug("Plugin constructed for session", session_id)
        self._network._send(_Messages.connect, [_Packet._has_brotli_compression(), original_version_table])
        self._run_text = "Run"
        self._run_usable = True
        self._advanced_settings_text = "Advanced Settings"
        self._advanced_settings_usable = True
