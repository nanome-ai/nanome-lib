from nanome._internal._network._commands._callbacks import _Messages
import nanome

class Stream(object):
    _streams = dict()

    def __init__(self, network, id):
        self.__network = network
        self.__id = id
        self.__interrupt_callback = None
        Stream._streams[id] = self

    def update(self, position_list, done_callback = None):
        """
        | Send positions to the stream, updating all its atoms

        :param position_list: List of positions for all atoms in the stream. There should be three floats per atom: x, y, and z
        :type position_list: list of :class:`float`
        """
        id = self.__network._send(_Messages.stream_feed, (self.__id, position_list))
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