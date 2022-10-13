from nanome.util import Logs
from nanome.util.stream import StreamInterruptReason


def _receive_interrupt_stream(network, result, request_id):
    from nanome.api.streams import Stream

    try:
        stream = Stream._streams[result[1]]
    except:
        Logs.warning("Got an error for an unknown stream. Probably tried to update an unknown stream:", result[1])
        return

    stream._interrupt(result[0])
