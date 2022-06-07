from nanome._internal._network._commands._callbacks import _Messages
import nanome
from nanome.util import Logs


class Stream(object):
    """
    | Class allowing a update or read properties of a lot of structures
    | Created by calling :func:`~nanome.PluginInstance.create_writing_stream` or :func:`~nanome.PluginInstance.create_reading_stream`

    | When created, a stream is linked to a number of structures. Each call to :func:`~update` will update all these structures
    """
    _streams = dict()

    Type = nanome.util.enums.StreamType
    DataType = nanome.util.enums.StreamDataType
    Direction = nanome.util.enums.StreamDirection

    def __init__(self, network, id, data_type, direction):
        self.id = id
        self.data_type = data_type
        self.direction = direction
        self.__network = network
        self.__interrupt_callback = lambda _: None
        self.__update_received = lambda _: None
        self.__warning_displayed = False
        Stream._streams[id] = self

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, value):
        self.__data_type = value

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value

    def update(self, data, done_callback=None):
        """
        | Send data to the stream, updating all its atoms

        :param data: List of data to send. i.e, for position stream: x, y, z, x, y, z, etc. (atom 1, atom 2, etc.)
        :type data: list of :class:`float` for position and scale streams, list of :class:`byte` for color streams
        """
        id = self.__network._send(_Messages.stream_feed, (self.__id, data, self.__data_type), done_callback is not None)
        if done_callback is None:
            def done_callback():
                return None
        nanome.PluginInstance._save_callback(id, done_callback)

    def set_on_interrupt_callback(self, callback):
        """
        | Sets the function to call if the stream gets interrupted (crash)
        """
        self.__interrupt_callback = callback

    def set_update_received_callback(self, callback):
        """
        | Sets the function to call if the stream is reading and received an update
        """
        self.__update_received = callback

    def destroy(self):
        """
        | Destroy stream once plugin doesn't need it anymore
        """
        del Stream._streams[self.__id]
        self.__network._send(_Messages.stream_destroy, self.__id, False)

    def _interrupt(self, reason):
        self.__interrupt_callback(reason)
        del Stream._streams[self.__id]

    def _update_received(self, data):
        if self.__update_received is None:
            if not self.__warning_displayed:
                Logs.warning("Received an update for a stream without received callback. Please call set_update_received_callback on stream creation")
                self.__warning_displayed = True
            return
        self.__update_received(data)
