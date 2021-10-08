def _feed_stream(network, result, request_id):
    from nanome.api.streams import Stream
    Stream._streams[result[0]]._update_received(result[1])
