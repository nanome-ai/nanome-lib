def _receive_controller_transforms(network, arg, request_id):
    network._call(request_id, *arg)
