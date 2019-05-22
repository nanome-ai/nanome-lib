def _add_dssp_done(network, result, request_id):
    network._call(request_id, result)
