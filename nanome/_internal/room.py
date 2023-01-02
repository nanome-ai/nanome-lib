from nanome._internal.network import PluginNetwork
from nanome._internal.network.commands.enums import Messages


class _Room():
    def __init__(self):
        pass

    def _set_skybox(self, skybox):
        PluginNetwork._send(Messages.set_skybox, skybox, False)
