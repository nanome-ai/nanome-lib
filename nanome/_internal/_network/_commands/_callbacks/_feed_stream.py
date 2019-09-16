def _feed_stream(network, result, request_id):
    nanome.util.Stream._streams[result[0]]._update_received(result[1])