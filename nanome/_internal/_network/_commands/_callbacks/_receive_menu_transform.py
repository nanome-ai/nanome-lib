def _receive_menu_transform(network, arg, request_id):
    network._call(request_id, *arg)
