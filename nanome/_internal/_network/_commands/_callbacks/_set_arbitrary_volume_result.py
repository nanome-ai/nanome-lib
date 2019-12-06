def _set_arbitrary_volume_result(network, result, request_id):
    network._call(request_id, result)