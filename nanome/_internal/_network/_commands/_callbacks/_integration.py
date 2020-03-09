from nanome.api.integration import Integration, IntegrationRequest


def _integration(network, args, request_id):
    integration = network._plugin.integration
    request = IntegrationRequest(args[0], args[1], args[2], network)
    Integration._send(integration, request)
