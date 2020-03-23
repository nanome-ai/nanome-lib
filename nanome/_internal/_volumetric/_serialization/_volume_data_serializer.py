from .. import _VolumeData
from nanome._internal._util._serializers import _TypeSerializer, _StringSerializer
from . import _UnitCellSerializer

class _VolumeDataSerializer(_TypeSerializer):
    __string = _StringSerializer()
    __cell = _UnitCellSerializer()

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "VolumeData"

    def serialize(self, version, value, context):
        context.write_int(value._width)
        context.write_int(value._height)
        context.write_int(value._depth)
        
        context.write_float(value._mean)
        context.write_float(value._rmsd)
        context.write_int(value._type)
        context.write_using_serializer(_VolumeDataSerializer.__string, value._name)
        context.write_using_serializer(_VolumeDataSerializer.__cell, value._cell)

        context.write_float_array(value._data)

    def deserialize(self, version, context):
        raise NotImplementedError
