from nanome._internal._network._commands._callbacks import _Messages
import nanome

class Stream(object):
    """
    | Class allowing a plugin to move a lot of atoms, several times per second if needed.
    | Created by calling :func:`~nanome.api.plugin_instance.PluginInstance.create_stream`

    | When created, a stream is linked to a number of atoms. Each call to :func:`~update` will update all these atoms
    """
    _streams = dict()

    Type = nanome.util.enums.StreamType
    DataType = nanome.util.enums.StreamDataType

    def __init__(self, network, id, data_type):
        self.__network = network
        self.__id = id
        self.__data_type = data_type
        self.__interrupt_callback = lambda _: None
        Stream._streams[id] = self

    def update(self, data, done_callback = None):
        """
        | Send data to the stream, updating all its atoms

        :param data: List of data to send. i.e, for position stream: x, y, z, x, y, z, etc. (atom 1, atom 2, etc.)
        :type data: list of :class:`float` for position and scale streams, list of :class:`byte` for color streams
        """
        id = self.__network._send(_Messages.stream_feed, (self.__id, data, self.__data_type))
        if done_callback == None:
            done_callback = lambda : None
        nanome.PluginInstance._save_callback(id, done_callback)

    def set_on_interrupt_callback(self, callback):
        """
        | Sets the function to call if the stream gets interrupted (crash)
        """
        self.__interrupt_callback = callback

    def destroy(self):
        """
        | Destroy stream once plugin doesn't need it anymore
        """
        del Stream._streams[self.__id]
        self.__network._send(_Messages.stream_destroy, self.__id)

    def _interrupt(self, reason):
        self.__interrupt_callback(reason)
        del Stream._streams[self.__id]