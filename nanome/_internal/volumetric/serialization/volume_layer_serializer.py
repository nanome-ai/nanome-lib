from .. import _VolumeData
from nanome._internal.util.type_serializers import TypeSerializer, ColorSerializer


class _VolumeLayerSerializer(TypeSerializer):
    __color = ColorSerializer()

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "VolumeLayer"

    def serialize(self, version, value, context):
        context.write_using_serializer(_VolumeLayerSerializer.__color, value._color)
        context.write_float(value._rmsd)

    def deserialize(self, version, context):
        raise NotImplementedError
