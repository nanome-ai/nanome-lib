def _receive_directory(network, result, request_id):
    network._call(request_id, result)

def _receive_file(network, file_list, request_id):
    network._call(request_id, file_list)

def _receive_file_save_result(network, result_list, request_id):
    network._call(request_id, result_list)