import fnmatch
import logging
import os
import signal
import sys
import subprocess
import time

logger = logging.getLogger(__name__)


class AutoReloadMixin(object):

    def __init__(self):
        super(AutoReloadMixin, self).__init__()
        self._pre_run = None
        self._post_run = None

    def autoreload(self):
        wait = 3

        if os.name == "nt":
            sub_kwargs = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP}
            break_signal = signal.CTRL_BREAK_EVENT
        else:
            sub_kwargs = {}
            break_signal = signal.SIGTERM

        # Make sure autoreload is turned off for child processes.
        sub_args = [x for x in sys.argv if x != '-r' and x != "--auto-reload"]
        popen_environ = dict(os.environ)
        popen_environ.pop('PLUGIN_AUTO_RELOAD', None)

        try:
            sub_args = [sys.executable] + sub_args
            process = subprocess.Popen(sub_args, env=popen_environ, **sub_kwargs)
        except Exception:
            logger.error("Couldn't find a suitable python executable")
            sys.exit(1)

        last_mtime = max(self.__file_times("."))
        while True:
            try:
                max_mtime = max(self.__file_times("."))
                if max_mtime > last_mtime:
                    last_mtime = max_mtime
                    logger.info("Restarting plugin")
                    process.send_signal(break_signal)
                    process = subprocess.Popen(sub_args, **sub_kwargs)
                time.sleep(wait)
            except KeyboardInterrupt:
                process.send_signal(break_signal)
                break

    def __file_times(self, path):
        found_file = False
        for root, dirs, files in os.walk(path):
            for file in filter(self.__file_filter, files):
                file_path = os.path.join(root, file)
                matched = False
                for pattern in self._to_ignore:
                    if fnmatch.fnmatch(file_path, pattern):
                        matched = True
                if matched is False:
                    found_file = True
                    yield os.stat(file_path).st_mtime
        if found_file is False:
            yield 0.0

    def __file_filter(self, name):
        return name.endswith(".py") or name.endswith(".json")

    @property
    def pre_run(self):
        """
        | Function to call before the plugin runs and tries to connect to NTS
        | Useful when using autoreload
        """
        return self._pre_run

    @pre_run.setter
    def pre_run(self, value):
        self._pre_run = value

    @property
    def post_run(self):
        """
        | Function to call when the plugin is about to exit
        | Useful when using autoreload
        """
        return self._post_run

    @post_run.setter
    def post_run(self, value):
        self._post_run = value
