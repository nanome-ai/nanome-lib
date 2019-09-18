def _receive_presenter_info(network, arg, request_id):
    network._call(request_id, arg)