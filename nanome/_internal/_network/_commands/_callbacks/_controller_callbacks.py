def _controller_response(network, arg, request_id):
    network._call(request_id, arg)