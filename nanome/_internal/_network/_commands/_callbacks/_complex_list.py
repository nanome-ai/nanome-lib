def _receive_complex_list(network, arg, request_id):
    network._call(request_id, arg)

def _receive_complexes(network, arg, request_id):
    for i in range(len(arg)):
        if arg[i]._index == -1:
            arg[i] = None
    network._call(request_id, arg)
