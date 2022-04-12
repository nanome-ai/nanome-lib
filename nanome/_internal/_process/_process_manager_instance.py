from nanome.util import Process, Logs
from . import ProcessManager

from collections import deque


class ProcessManagerInstance():

    def __init__(self, pipe):
        self.__pipe = pipe
        Process.manager = self
        self.__pending_start = deque()
        self.__processes = dict()

    def start_process(self, process, request):
        self.__pending_start.append(process)
        self.send(ProcessManager.CommandType.start, request)

    def stop_process(self, process):
        self.send(ProcessManager.CommandType.stop, process.id)

    def send(self, type, data):
        from nanome._internal._util import ProcData
        to_send = ProcData()
        to_send._data = [type, data]
        self.__pipe.send(to_send)

    def update(self):
        has_data = None
        try:
            has_data = self.__pipe.poll()
            if has_data:
                data = self.__pipe.recv()
        except BrokenPipeError:
            Logs.message("Pipe has been closed, exiting process")
            return False
        except EOFError:
            Logs.message("Pipe has been closed by user, exiting process")
            return False
        if has_data:
            self.__received_data(data)
        return True

    def __received_data(self, data):
        type = data[0]
        if type == ProcessManager.DataType.queued:
            process = self.__pending_start.popleft()
            process.on_queued()
            process.id = data[1].id
            self.__processes[data[1].id] = process
        elif type == ProcessManager.DataType.position_changed:
            self.__processes[data[1]].on_queue_position_change(data[2])
        elif type == ProcessManager.DataType.starting:
            self.__processes[data[1]].on_start()
        elif type == ProcessManager.DataType.done:
            process = self.__processes[data[1]]
            if process._future is not None:
                process._future.set_result(data[2])
            process.on_done(data[2])
        elif type == ProcessManager.DataType.error:
            self.__processes[data[1]].on_error(data[2])
        elif type == ProcessManager.DataType.output:
            self.__processes[data[1]].on_output(data[2])
        else:
            Logs.error("Received unknown process data type")
    
    def _close(self):
        try:
            self.__pipe.close()
        except BrokenPipeError:
            pass
