def _receive_macros(network, arg, request_id):
    network._call(request_id, arg)