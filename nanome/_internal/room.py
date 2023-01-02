import nanome
from nanome._internal.network import PluginNetwork
from nanome._internal.network.commands.callbacks import Messages


class _Room():
    SkyBoxes = nanome.util.enums.SkyBoxes

    def __init__(self):
        pass

    def _set_skybox(self, skybox):
        PluginNetwork._send(Messages.set_skybox, skybox, False)
