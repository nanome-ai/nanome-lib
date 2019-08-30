import nanome
from nanome.util import Logs
from nanome._internal._network import _ProcessNetwork, _Packet
from nanome._internal._process import _ProcessManagerInstance
from nanome._internal._network._commands._callbacks import _Messages

import traceback
import time
from timeit import default_timer as timer

UPDATE_RATE = 1.0 / 60.0
MINIMUM_SLEEP = 0.001

__metaclass__ = type
class _PluginInstance(object):
    __callbacks = dict()

    @classmethod
    def _save_callback(cls, id, callback):
        if callback == None:
            cls.__callbacks[id] = lambda _=None: None
        else:
            cls.__callbacks[id] = callback

    def _call(self, id, *args):
        callbacks = _PluginInstance.__callbacks
        try:
            callbacks[id](*args)
            del callbacks[id]
        except KeyError:
            Logs.warning('Received an unknown callback id:', id)

    def _run(self):
        try:
            self.start()
            last_update = timer()
            while self._network._receive() and self._process_manager.update():
                self.update()

                dt = last_update - timer()
                sleep_time = max(UPDATE_RATE - dt, MINIMUM_SLEEP)
                time.sleep(sleep_time)
                last_update = timer()

        except KeyboardInterrupt:
            return
        except:
            Logs.error(traceback.format_exc())
            self._process_manager._close()
            self._network._close()
            return

    def __init__(self, session_id, net_pipe, proc_pipe, serializer, plugin_id, version_table, original_version_table, verbose):
        Logs._set_verbose(verbose)

        self._network = _ProcessNetwork(self, session_id, net_pipe, serializer, plugin_id, version_table)
        self._process_manager = _ProcessManagerInstance(proc_pipe)
        Logs.debug("Plugin constructed for session", session_id)
        self._network._send(_Messages.connect, [_Packet._compression_type(), original_version_table])
        self._run_text = "Run"
        self._run_usable = True
        self._advanced_settings_text = "Advanced Settings"
        self._advanced_settings_usable = True