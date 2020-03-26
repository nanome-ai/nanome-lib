from .. import _VolumeData
from nanome._internal._util._serializers import _TypeSerializer, _ArraySerializer
from . import _VolumeLayerSerializer

class _VolumePropertiesSerializer(_TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_VolumeLayerSerializer())

    def version(self):
        return 0

    def name(self):
        return "VolumeProperties"

    def serialize(self, version, value, context):
        context.write_bool(value._visible)
        context.write_bool(value._boxed)
        context.write_bool(value._use_map_mover)
        context.write_int(int(value._style))
        context.write_using_serializer(self.__array, value._layers)

    def deserialize(self, version, context):
        raise NotImplementedError
