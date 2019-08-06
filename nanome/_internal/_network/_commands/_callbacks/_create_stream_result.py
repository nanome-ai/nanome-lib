from nanome.api.streams import Stream
from nanome.util.stream import StreamCreationError
from nanome.util import Logs

def _receive_create_stream_result(network, result, request_id):
    if result[0] != StreamCreationError.NoError:
        network._call(request_id, None, result[0])
        return
    stream = Stream(network, result[1], result[2])
    network._call(request_id, stream, StreamCreationError.NoError)