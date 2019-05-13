def _controller_response(network, arg, request_id):
    network._call(request_id, arg)

def _controller_callback(network, arg, request_id):
    #expects arg to be a tuple of the order:
    #controller_type, controller_button, controller_event, controller
    network._plugin.user._on_controller_callback(arg[0],arg[1],arg[2],arg[3])