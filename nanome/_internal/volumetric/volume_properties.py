from nanome.util import enums


class _VolumeProperties():
    VolumeVisualStyle = enums.VolumeVisualStyle

    def __init__(self):
        self._visible = True
        self._boxed = True
        self._use_map_mover = True
        self._style = _VolumeProperties.VolumeVisualStyle.Mesh
        self._layers = []
