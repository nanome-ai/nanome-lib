
from . import Integration, IntegrationRequest
from nanome.api._hashes import Hashes


def integration(network, args, request_id):
    integration = network._plugin.integration
    request = IntegrationRequest(args[0], args[1], args[2], network)
    name = Hashes.HashToIntegrationName[args[1]]
    Integration._call(integration, name, request)
