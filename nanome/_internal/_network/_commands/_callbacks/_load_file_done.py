def _load_file_done(network, result, request_id):
    network._call(request_id, result)
