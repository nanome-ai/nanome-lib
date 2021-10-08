import nanome
from nanome.util import Logs
from nanome._internal._network import _ProcessNetwork, _Packet
from nanome._internal._process import _ProcessManagerInstance
from nanome._internal._network._commands._callbacks import _Messages
from nanome._internal._network._commands._callbacks._commands_enums import _Hashes

import traceback
import time
from timeit import default_timer as timer

try:
    import asyncio
    from ._plugin_instance_async import _async_update_loop
except ImportError:
    asyncio = False

UPDATE_RATE = 1.0 / 60.0
MINIMUM_SLEEP = 0.001

__metaclass__ = type


class _PluginInstance(object):
    __callbacks = dict()
    __futures = dict()
    __complex_updated_callbacks = dict()
    __selection_changed_callbacks = dict()

    @classmethod
    def _save_callback(cls, id, callback):
        if callback is None:
            if asyncio and nanome.PluginInstance._instance.is_async:
                loop = asyncio.get_event_loop()
                future = loop.create_future()
                cls.__futures[id] = future
                return future
            else:
                cls.__callbacks[id] = lambda *_: None
        else:
            cls.__callbacks[id] = callback

    def _call(self, id, *args):
        callbacks = _PluginInstance.__callbacks
        futures = _PluginInstance.__futures

        if asyncio and self.is_async and futures.get(id):
            futures[id].set_result(args[0] if len(args) == 1 else args)
            del futures[id]
            return

        if id not in callbacks:
            Logs.warning('Received an unknown callback id:', id)
            return

        callbacks[id](*args)
        del callbacks[id]

    @classmethod
    def _hook_complex_updated(cls, index, callback):
        cls.__complex_updated_callbacks[index] = callback

    @classmethod
    def _hook_selection_changed(cls, index, callback):
        cls.__selection_changed_callbacks[index] = callback

    @classmethod
    def _on_complex_updated(cls, index, new_complex):
        callbacks = _PluginInstance.__complex_updated_callbacks
        try:
            callbacks[index](new_complex)
        except KeyError:
            Logs.warning('Received an unknown updated complex index:', index)

    @classmethod
    def _on_selection_changed(cls, index, new_complex):
        callbacks = _PluginInstance.__selection_changed_callbacks
        try:
            callbacks[index](new_complex)
        except KeyError:
            Logs.warning('Received an unknown updated complex index:', index)

    def _on_stop(self):
        try:
            self.on_stop()
        except:
            Logs.error("Error in on_stop function:", traceback.format_exc())

    def _update_loop(self):
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
            self._on_stop()
            return
        except:
            Logs.error(traceback.format_exc())
            self._on_stop()
            self._process_manager._close()
            self._network._close()
            return

    def _run(self):
        if asyncio and self.is_async:
            coro = _async_update_loop(self, UPDATE_RATE, MINIMUM_SLEEP)
            asyncio.run(coro)
        else:
            self._update_loop()

    def _has_permission(self, permission):
        return _Hashes.PermissionRequestHashes[permission] in self._permissions

    def __init__(self, session_id, net_pipe, proc_pipe, serializer, plugin_id, version_table, original_version_table, verbose, custom_data, permissions):
        Logs._set_verbose(verbose)
        Logs._set_pipe(proc_pipe)
        self._menus = {}

        self._network = _ProcessNetwork(self, session_id, net_pipe, serializer, plugin_id, version_table)
        self._process_manager = _ProcessManagerInstance(proc_pipe)

        Logs.debug("Plugin constructed for session", session_id)
        self._network._send_connect(_Messages.connect, [_Packet._compression_type(), original_version_table])
        self._run_text = "Run"
        self._run_usable = True
        self._advanced_settings_text = "Advanced Settings"
        self._advanced_settings_usable = True
        self._custom_data = custom_data
        self._permissions = permissions
