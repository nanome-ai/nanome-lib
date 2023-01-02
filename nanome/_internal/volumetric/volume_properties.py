class _VolumeProperties():

    def __init__(self):
        from nanome.util import enums
        self._visible = True
        self._boxed = True
        self._use_map_mover = True
        self._style = enums.VolumeVisualStyle.Mesh
        self._layers = []
