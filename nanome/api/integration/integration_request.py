from nanome._internal._network._commands._callbacks._commands_enums import _Messages

class IntegrationRequest():
    def __init__(self, request_id, type, args, network):
        self.__request_id = request_id
        self.__type = type
        self.__args = args
        self.__network = network

    def get_args(self):
        return self.__args

    def send_response(self, args):
        response = (self.__request_id, self.__type, args)
        self.__network._send(_Messages.integration, response, False)
