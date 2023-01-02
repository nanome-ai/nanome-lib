from nanome._internal.network.commands.callbacks.commands_enums import Hashes


def _integration(network, args, request_id):
    from nanome.api.integration import Integration, IntegrationRequest

    integration = network._plugin.integration
    request = IntegrationRequest(args[0], args[1], args[2], network)
    name = Hashes.HashToIntegrationName[args[1]]
    Integration._call(integration, name, request)
