from nanome.api.streams import Stream

def _feed_stream(network, result, request_id):
    Stream._streams[result[0]]._update_received(result[1])