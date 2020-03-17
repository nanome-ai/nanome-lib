def _simple_callback_arg_unpack(network, arg, request_id):
    network._call(request_id, *arg)

def _simple_callback_arg(network, arg, request_id):
    network._call(request_id, arg)

def _simple_callback_no_arg(network, arg, request_id):
    network._call(request_id)