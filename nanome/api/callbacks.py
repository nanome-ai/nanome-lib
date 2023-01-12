import logging
from ._hashes import Hashes

from nanome.api.integration import Integration, IntegrationRequest


logger = logging.getLogger(__name__)


def advanced_settings(network, args, request_id):
    network.on_advanced_settings()


def connect(network, arg, request_id):
    pass


def integration(network, args, request_id):
    integration = network._plugin.integration
    request = IntegrationRequest(args[0], args[1], args[2], network)
    name = Hashes.HashToIntegrationName[args[1]]
    Integration._call(integration, name, request)


def run(network, args, request_id):
    network._on_run()


def simple_callback_arg_unpack(network, arg, request_id):
    network._call(request_id, *arg)


def simple_callback_arg(network, arg, request_id):
    network._call(request_id, arg)


def simple_callback_no_arg(network, arg, request_id):
    network._call(request_id)

