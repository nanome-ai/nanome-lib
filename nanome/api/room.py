import nanome
from nanome._internal._room import _Room


class Room(_Room):
    """
    | Represents a room in Nanome
    """
    SkyBoxes = nanome.util.enums.SkyBoxes

    def __init__(self):
        self._skybox = Room.SkyBoxes.Unknown

    def set_skybox(self, skybox):
        self._set_skybox(skybox)
