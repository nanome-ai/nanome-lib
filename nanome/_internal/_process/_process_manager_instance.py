from nanome.util import Process, Logs
from . import _ProcessManager

from collections import deque


class _ProcessManagerInstance():
    def __init__(self, pipe):
        self.__pipe = pipe
        Process._manager = self
        self.__pending_start = deque()
        self.__processes = dict()

    def _close(self):
        self.__pipe.close()

    def update(self):
        has_data = None
        try:
            has_data = self.__pipe.poll()
            if has_data:
                data = self.__pipe.recv()
        except BrokenPipeError:
            Logs.debug("Pipe has been closed, exiting process")
            return False
        if has_data:
            self.__received_data(data)
        return True

    def __received_data(self, data):
        type = data[0]
        if type == _ProcessManager._DataType.queued:
            process = self.__pending_start.popleft()
            process.on_queued()
            process._id = data[1].id
            self.__processes[data[1].id] = process
        elif type == _ProcessManager._DataType.position_changed:
            self.__processes[data[1]].on_queue_position_change(data[2])
        elif type == _ProcessManager._DataType.starting:
            self.__processes[data[1]].on_start()
        elif type == _ProcessManager._DataType.done:
            self.__processes[data[1]].on_done(data[2])
        elif type == _ProcessManager._DataType.error:
            self.__processes[data[1]].on_error(data[2])
        elif type == _ProcessManager._DataType.output:
            self.__processes[data[1]].on_output(data[2])
        else:
            Logs.error("Received unknown process data type")

    def start_process(self, process, request):
        self.__pending_start.append(process)
        self.send(_ProcessManager._CommandType.start, request)

    def stop_process(self, process):
        self.send(_ProcessManager._CommandType.stop, process._id)

    def send(self, type, data):
        from nanome._internal._util import _ProcData
        to_send = _ProcData()
        to_send._data = [type, data]
        self.__pipe.send(to_send)
