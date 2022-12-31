from collections import deque
from functools import partial
import subprocess
import traceback
import sys
import time
from threading import Thread

try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty  # python 2.x

from nanome._internal._process import ProcessEntry
from nanome.util import Logs, IntEnum, auto

POSIX = 'posix' in sys.builtin_module_names


class ProcessManager():

    class DataType(IntEnum):
        queued = auto()
        position_changed = auto()
        starting = auto()
        error = auto()
        output = auto()
        done = auto()

    class CommandType(IntEnum):
        start = auto()
        stop = auto()

    _max_process_count = 10

    def __init__(self):
        self.__pending = deque()
        self.__running = []

    def update(self):
        try:
            for i in range(len(self.__running) - 1, -1, -1):
                proc = self.__running[i]
                if self.__update_process(proc) == False:
                    del self.__running[i]

            spawn_count = min(ProcessManager._max_process_count - len(self.__running), len(self.__pending))
            if spawn_count > 0:
                while spawn_count > 0:
                    self.__start_process()
                    spawn_count -= 1

                count_before_exec = 1
                for entry in self.__pending:
                    entry.send(ProcessManager.DataType.position_changed, [count_before_exec])
                    count_before_exec += 1
        except:
            Logs.error("Exception in process manager update:\n", traceback.format_exc())

    def __start_process(self):
        entry = self.__pending.popleft()
        entry.send(ProcessManager.DataType.starting, [])
        request = entry.request
        args = [request.executable_path] + request.args
        has_text = entry.output_text

        def enqueue_output(pipe, queue, text, bufsize):
            if text:
                sentinel = ''
            else:
                sentinel = b''

            read_fn = pipe.readline if bufsize == 1 else partial(pipe.read, 1)
            for data in iter(read_fn, sentinel):
                queue.put(data)
            pipe.close()

        try:
            # Log process settings
            exec_path = request.executable_path
            session_id = entry.session._session_id

            entry.process = subprocess.Popen(
                args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=request.bufsize,
                cwd=request.cwd_path, encoding=request.encoding, universal_newlines=has_text,
                close_fds=POSIX)
            entry.start_time = time.time()

            id = request.label or exec_path
            extra = {
                'process_args': args,
                'executable_path': exec_path,
                'session_id': session_id,
                'request_id': request.id,
                'process_label': request.label
            }
            msg = "Process Started: {} for Session {}".format(id, session_id)
            Logs.message(msg, extra=extra)
        except:
            Logs.error("Couldn't execute process", exec_path, "Please check if executable is present and has permissions:\n", traceback.format_exc())
            entry.send(ProcessManager.DataType.done, [-1])
            return
        entry.stdout_queue = Queue()
        entry.stderr_queue = Queue()
        thread_out = Thread(target=enqueue_output, args=(entry.process.stdout, entry.stdout_queue, has_text, request.bufsize), daemon=True)
        thread_err = Thread(target=enqueue_output, args=(entry.process.stderr, entry.stderr_queue, has_text, request.bufsize), daemon=True)
        thread_out.start()
        thread_err.start()
        self.__running.append(entry)

    def __update_process(self, entry):
        # Process stdout and stderr
        if entry.output_text:
            output = ""
            error = ""
        else:
            output = b""
            error = b""
        try:
            while True:
                output += entry.stdout_queue.get_nowait()
        except Empty:
            pass
        try:
            while True:
                error += entry.stderr_queue.get_nowait()
        except Empty:
            pass

        if error:
            entry.send(ProcessManager.DataType.error, [error])

        if output:
            entry.send(ProcessManager.DataType.output, [output])

        # Check if timeout occurred
        timeout = getattr(entry.request, 'timeout')
        if timeout and time.time() - entry.start_time > timeout:
            entry.process.kill()

        # Check if process finished
        exit_code = entry.process.poll()
        if exit_code is not None:
            # Finish process
            # Log completion data
            end_time = time.time()
            elapsed_time = round(end_time - entry.start_time, 3)
            exec_path = entry.request.executable_path
            request_id = entry.request.id
            session_id = entry.session._session_id
            label = entry.request.label
            id = label or exec_path
            message = "Process Completed: {} for Session {} returned exit code {} in {}s".format(
                id, session_id, exit_code, elapsed_time)
            log_extra = {
                'request_id': request_id,
                'executable_path': exec_path,
                'process_time': elapsed_time,
                'exit_code': exit_code,
                'session_id': session_id,
                'process_label': label
            }
            if exit_code == 0:
                Logs.message(message, extra=log_extra)
            else:
                Logs.warning(message, extra=log_extra)
            entry.send(ProcessManager.DataType.done, [exit_code])
            return False
        return True

    def __stop_process(self, id):
        for entry in self.__running:
            if entry.request.id == id:
                entry.process.terminate()
                break

    def _remove_session_processes(self, session_id):
        pending = [e for e in self.__pending if e.session._session_id == session_id]
        running = [e for e in self.__running if e.session._session_id == session_id]

        for entry in pending:
            self.__pending.remove(entry)

        for entry in running:
            entry.process.kill()
            self.__running.remove(entry)

    def received_request(self, data, session):
        type = data[0]
        process_request = data[1]
        if type == ProcessManager.CommandType.start:
            request = process_request
            entry = ProcessEntry(request, session)
            self.__pending.append(entry)
            session.send_process_data([ProcessManager.DataType.queued, request])
        elif type == ProcessManager.CommandType.stop:
            self.__stop_process(process_request)
        else:
            Logs.error("Received unknown process command type")
