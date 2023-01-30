from nanome.util import enums
from nanome._internal.network import PluginNetwork
from nanome._internal.enums import Messages


class Room:
    """
    | Represents a room in Nanome
    """
    SkyBoxes = enums.SkyBoxes

    def __init__(self):
        self._skybox = Room.SkyBoxes.Unknown

    def set_skybox(self, skybox):
        self._set_skybox(skybox)

    def _set_skybox(self, skybox):
        PluginNetwork._instance.send(Messages.set_skybox, skybox, False)
