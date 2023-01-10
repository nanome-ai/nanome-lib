import logging
import os
import traceback
import time
from timeit import default_timer as timer

from nanome._internal.network import Packet
from nanome._internal.process import ProcessManagerInstance
from nanome._internal.enums import Hashes, Messages
from nanome._internal.util.decorators import deprecated
from nanome._internal import shapes as internal_shapes

logger = logging.getLogger(__name__)

try:
    import asyncio
    from .plugin_instance_async import async_update_loop
except ImportError:
    asyncio = False

UPDATE_RATE = 1.0 / 60.0
MINIMUM_SLEEP = 0.001

# End session after 12 hours by default
# This should be long enough to indicate
# a runaway session that wasn't closed by NTS
default_session_timeout = 12 * 60 * 60
env_var_session_timeout = os.environ.get('SESSION_TIMEOUT')
if env_var_session_timeout and env_var_session_timeout.isdigit():
    SESSION_TIMEOUT = int(env_var_session_timeout)
else:
    SESSION_TIMEOUT = default_session_timeout


__metaclass__ = type


class _PluginInstance(object):
    __callbacks = dict()
    __futures = dict()
    __complex_updated_callbacks = dict()
    __selection_changed_callbacks = dict()

    def _setup(
        self, session_id, plugin_network, pm_queue_in, pm_queue_out, log_pipe_conn,
            original_version_table, custom_data, permissions):
        self._menus = {}
        self._run_text = "Run"
        self._run_usable = True
        self._advanced_settings_text = "Advanced Settings"
        self._advanced_settings_usable = True
        self._custom_data = custom_data
        self._permissions = permissions
        self._session_timeout = SESSION_TIMEOUT

        self._network = plugin_network
        self._process_manager = ProcessManagerInstance(pm_queue_in, pm_queue_out)
        self._log_pipe_conn = log_pipe_conn
        self._network.send_connect(Messages.connect, [Packet._compression_type(), original_version_table])
        logger.debug("Plugin constructed for session {}".format(session_id))

    @classmethod
    def _save_callback(cls, id, callback):
        if callback is None:
            import nanome
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
        callbacks = self.__callbacks
        futures = self.__futures

        if asyncio and self.is_async and futures.get(id):
            futures[id].set_result(args[0] if len(args) == 1 else args)
            del futures[id]
            return

        if id not in callbacks:
            logger.warning('Received an unknown callback id: {}'.format(id))
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
        callbacks = cls.__complex_updated_callbacks
        try:
            callbacks[index](new_complex)
        except KeyError:
            logger.warning('Received an unknown updated complex index: {}'.format(index))

    @classmethod
    def _on_selection_changed(cls, index, new_complex):
        callbacks = cls.__selection_changed_callbacks
        try:
            callbacks[index](new_complex)
        except KeyError:
            logger.warning('Received an unknown updated complex index: {index}')

    def _on_stop(self):
        try:
            self.on_stop()
        except:
            logger.error("Error in on_stop function:", traceback.format_exc())

    def _update_loop(self):
        try:
            self.start()
            loop_start_time = timer()
            last_update = timer()
            while self._network._receive() and self._process_manager.update():
                self.update()

                dt = last_update - timer()
                sleep_time = max(UPDATE_RATE - dt, MINIMUM_SLEEP)
                time.sleep(sleep_time)
                last_update = timer()
                if last_update - loop_start_time > self._session_timeout:
                    raise TimeoutError()
        except KeyboardInterrupt:
            self._on_stop()
            return
        except TimeoutError:
            logger.warning("Session timed out")
            self._on_stop()
            self._process_manager._close()
            self._network._close()
            return
        except Exception as e:
            text = ' '.join(map(str, e.args))
            msg = "Uncaught " + type(e).__name__ + ": " + text
            logger.error(msg)
            # Give log a little time to reach destination before closing pipe
            time.sleep(0.1)
            self._on_stop()
            self._process_manager._close()
            self._network._close()
            return

    def _run(self):
        if asyncio and self.is_async:
            coro = async_update_loop(self, UPDATE_RATE, MINIMUM_SLEEP)
            asyncio.run(coro)
        else:
            self._update_loop()

    def _has_permission(self, permission):
        return Hashes.PermissionRequestHashes[permission] in self._permissions

    @deprecated("files.ls")
    def request_directory(self, path, callback=None, pattern="*"):
        """
        | Requests the content of a directory on the machine running Nanome

        :param path: Path to request. E.g. "." means Nanome's running directory
        :type path: str
        :param pattern: Pattern to match. E.g. "*.txt" will match all .txt files. Default value is "*" (match everything)
        :type pattern: str
        """
        from nanome.util import DirectoryRequestOptions
        options = DirectoryRequestOptions()
        options._directory_name = path
        options._pattern = pattern
        id = self._network.send(Messages.directory_request, options, callback != None)
        self._save_callback(id, callback)

    @deprecated("files.get")
    def request_files(self, file_list, callback=None):
        """
        | Reads files on the machine running Nanome, and returns them

        :param file_list: List of file name (with path) to read. E.g. ["a.sdf", "../b.sdf"] will read a.sdf in running directory, b.sdf in parent directory, and return them
        :type file_list: list of :class:`str`
        """
        id = self._network.send(Messages.file_request, file_list, callback != None)
        self._save_callback(id, callback)

    @deprecated()
    def create_shape(self, shape_type):
        from nanome.util.enums import ShapeType
        if shape_type == ShapeType.Sphere:
            return internal_shapes._Sphere._create()
        if shape_type == ShapeType.Line:
            return internal_shapes._Line._create()
        raise ValueError('Parameter shape_type must be a value of nanome.util.enums.ShapeType')
