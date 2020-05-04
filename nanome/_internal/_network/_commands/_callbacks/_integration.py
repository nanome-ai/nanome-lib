from nanome._internal._network._commands._callbacks._commands_enums import _Hashes

def _integration(network, args, request_id):
    from nanome.api.integration import Integration, IntegrationRequest

    integration = network._plugin.integration
    request = IntegrationRequest(args[0], args[1], args[2], network)
    name = _Hashes.HashToIntegrationName[args[1]]
    Integration._call(integration, name, request)
