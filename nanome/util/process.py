import subprocess
import nanome
import sys

asyncio = False
if sys.version_info >= (3, 7):
    try:
        import asyncio
    except ImportError:
        pass


class Process():
    """
    | A command-line process wrapper.
    """
    _manager = None

    class _ProcessRequest():
        def __init__(self):
            self.executable_path = ""
            self.args = []
            self.encoding = None  # "utf-8" if stdout and err are text
            self.bufsize = 1
            self.cwd_path = None
            self.id = 0

    def __init__(self, executable_path=None, args=None, output_text=None, buffer_lines=True):
        self.on_queued = lambda: None
        self.on_queue_position_change = lambda _: None
        self.on_start = lambda: None
        self.on_done = lambda _: None
        self.on_error = lambda _: None
        self.on_output = lambda _: None
        self._future = None
        self.__request = Process._ProcessRequest()

        if executable_path is not None:
            self.executable_path = executable_path
        if args is not None:
            self.args = args
        if output_text is not None:
            self.output_text = output_text
        self.buffer_lines = buffer_lines

    @property
    def executable_path(self):
        """
        | The path to the executable to be run.

        :type: :class:`str`
        """
        return self.__request.executable_path

    @executable_path.setter
    def executable_path(self, value):
        self.__request.executable_path = value

    @property
    def args(self):
        """
        | A list of arguments to pass to the executable.

        :type: :class:`list` <:class:`str`>
        """
        return self.__request.args

    @args.setter
    def args(self, value):
        self.__request.args = value

    @property
    def cwd_path(self):
        """
        | The working directory path where the process will be/was executed.

        :type: :class:`str`
        """
        return self.__request.cwd_path

    @cwd_path.setter
    def cwd_path(self, value):
        self.__request.cwd_path = value

    @property
    def output_text(self):
        """
        | Whether or not the process will produce text output.

        :type: :class:`bool`
        """
        return self.__request.encoding == "utf-8"

    @output_text.setter
    def output_text(self, value):
        self.__request.encoding = "utf-8" if value else None

    @property
    def buffer_lines(self):
        """
        | Whether or not to buffer output by lines.

        :type: :class:`bool`
        """
        return self.__request.bufsize == 1

    @buffer_lines.setter
    def buffer_lines(self, value):
        self.__request.bufsize = 1 if value else 0

    @property
    def _id(self):
        return self.__request.id

    @_id.setter
    def _id(self, value):
        self.__request.id = value

    def start(self):
        """
        | Starts the process.
        """

        if asyncio and nanome.PluginInstance._instance.is_async:
            loop = asyncio.get_event_loop()
            future = loop.create_future()
            self._future = future

        if self._manager is None:
            nanome.util.Logs.warning("Running process outside of ProcessManager. This should only happen during unittests.")
            cmd = [self.executable_path] + self.args
            result = subprocess.run(cmd, capture_output=True, text=self.output_text)
            self.on_output(result.stdout)
            self.on_error(result.stderr)
            self._future.set_result(result.returncode)
        else:
            Process._manager.start_process(self, self.__request)
        return self._future

    def stop(self):
        """
        | Stops the process.
        """
        Process._manager.stop_process(self)
