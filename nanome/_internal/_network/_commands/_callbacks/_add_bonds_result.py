def _add_bonds_result(network, result, request_id):
    network._call(request_id, result)