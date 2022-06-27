from nanome.util import Process, Logs
from . import ProcessManager

from collections import deque


class ProcessManagerInstance():

    def __init__(self, queue_in, queue_out):
        self.__queue_in = queue_in
        self.__queue_out = queue_out
        Process._manager = self
        self.__pending_start = deque()
        self.__processes = dict()

    def start_process(self, process, request):
        self.__pending_start.append(process)
        self.send(ProcessManager.CommandType.start, request)

    def stop_process(self, process):
        self.send(ProcessManager.CommandType.stop, process.id)

    def send(self, type, data):
        proc_data = [type, data]
        self.__queue_out.put(proc_data)

    def update(self):
        has_data = None
        try:
            has_data = not self.__queue_in.empty()
            if has_data:
                data = self.__queue_in.get()
        except Exception:
            Logs.message("Queue has been closed, exiting process")
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

        if type == ProcessManager.DataType.queued:
            process = self.__pending_start.popleft()
            process.on_queued()
            process.id = process_request.id
            self.__processes[process_request.id] = process
        elif type == ProcessManager.DataType.position_changed:
            self.__processes[process_request].on_queue_position_change(output)
        elif type == ProcessManager.DataType.starting:
            self.__processes[process_request].on_start()
        elif type == ProcessManager.DataType.done:
            process = self.__processes[process_request]
            if process._future is not None:
                process._future.set_result(output)
            process.on_done(output)
        elif type == ProcessManager.DataType.error:
            self.__processes[process_request].on_error(output)
        elif type == ProcessManager.DataType.output:
            self.__processes[process_request].on_output(output)
        else:
            Logs.error("Received unknown process data type")

    def _close(self):
        try:
            self.__queue_out.close()
        except Exception:
            pass
