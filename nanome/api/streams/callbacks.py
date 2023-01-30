from . import Stream
from nanome.util.stream import StreamCreationError
from nanome.util import Logs


def feed_stream(network, result, request_id):
    Stream._streams[result[0]]._update_received(result[1])


def receive_create_stream_result(network, result, request_id):
    if result[0] != StreamCreationError.NoError:
        network._call(request_id, None, result[0])

        if result[0] == StreamCreationError.UnsupportedStream:
            Logs.error("Tried to create an unsupported type of stream")
        return

    stream = Stream(network, result[1], result[2], result[3])
    network._call(request_id, stream, StreamCreationError.NoError)


def receive_interrupt_stream(network, result, request_id):
    try:
        stream = Stream._streams[result[1]]
    except:
        Logs.warning(
            ("Got an error for an unknown stream."
             "Probably tried to update an unknown stream: {}".format(result[1]))
        )
        return
    stream._interrupt(result[0])
