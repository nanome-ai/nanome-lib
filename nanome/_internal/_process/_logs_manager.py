from collections import deque
import logging
from logging.handlers import RotatingFileHandler
from nanome.util import Logs

class _LogsManager():
    __pending = deque()

    def __init__(self, filename):
        self.__logger = logging.getLogger('plugin_logger')
        self.__logger.setLevel(logging.DEBUG)
        self.__handler = RotatingFileHandler(filename, maxBytes=1048576, backupCount=3, delay=False)
        self.__logger.addHandler(self.__handler)

    def _update(self):
        for _ in range(0, len(_LogsManager.__pending)):
            entry = _LogsManager.__pending.popleft()
            if entry._type == Logs._LogType.debug:
                self.__logger.info(entry._msg)
            elif entry._type == Logs._LogType.warning:
                self.__logger.warning(entry._msg)
            elif entry._type == Logs._LogType.error:
                self.__logger.error(entry._msg)

    @classmethod
    def _received_request(cls, request):
        cls.__pending.append(request)