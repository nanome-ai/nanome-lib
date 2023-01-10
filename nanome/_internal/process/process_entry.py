class ProcessEntry():
    _current_process_id = 0

    def __init__(self, request, session):
        request.id = ProcessEntry._current_process_id
        ProcessEntry._current_process_id += 1
        self.__request = request
        self.__session = session
        self.__process = None
        self.__output_text = request.encoding != None
        self.stdout_queue = None
        self.stderr_queue = None
        self.start_time = None

    def send(self, type, data):
        self.__session.send_process_data([type, self.__request.id] + data)

    @property
    def request(self):
        return self.__request

    @property
    def session(self):
        return self.__session

    @property
    def output_text(self):
        return self.__output_text

    @property
    def process(self):
        return self.__process

    @process.setter
    def process(self, value):
        self.__process = value
