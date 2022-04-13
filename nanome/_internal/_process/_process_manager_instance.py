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
        try:
            self.__pipe.close()
        except BrokenPipeError:
            pass

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
        process_request = data[1]
        output = None
        if len(data) > 2:
            output = data[2]

        if type == _ProcessManager._DataType.queued:
            process = self.__pending_start.popleft()
            process.on_queued()
            process.id = process_request.id
            self.__processes[process_request.id] = process
        elif type == _ProcessManager._DataType.position_changed:
            self.__processes[process_request].on_queue_position_change(output)
        elif type == _ProcessManager._DataType.starting:
            self.__processes[process_request].on_start()
        elif type == _ProcessManager._DataType.done:
            process = self.__processes[process_request]
            if process._future is not None:
                process._future.set_result(output)
            process.on_done(output)
        elif type == _ProcessManager._DataType.error:
            self.__processes[process_request].on_error(output)
        elif type == _ProcessManager._DataType.output:
            self.__processes[process_request].on_output(output)
        else:
            Logs.error("Received unknown process data type")

    def start_process(self, process, request):
        self.__pending_start.append(process)
        self.send(_ProcessManager._CommandType.start, request)

    def stop_process(self, process):
        self.send(_ProcessManager._CommandType.stop, process._id)

    def send(self, type, data):
        to_send = [type, data]
        self.__pipe.send(to_send)
