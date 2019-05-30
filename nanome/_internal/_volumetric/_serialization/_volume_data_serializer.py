from .. import _VolumeData
from nanome._internal._util._serializers import _TypeSerializer

class _VolumeDataSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "VolumeData"

    def serialize(self, version, value, context):

        context.write_int(value._size_x)
        context.write_int(value._size_y)
        context.write_int(value._size_z)
        
        context.write_float(value._delta_x)
        context.write_float(value._delta_y)
        context.write_float(value._delta_z)

        context.write_float(value._origin_x)
        context.write_float(value._origin_y)
        context.write_float(value._origin_z)

        context.write_float_array(value._data)

    def deserialize(self, version, context):
        result = _VolumeData(0,0,0,0,0,0)

        result._size_x = context.read_int()
        result._size_y = context.read_int()
        result._size_z = context.read_int()
        
        result._delta_x = context.read_float()
        result._delta_y = context.read_float()
        result._delta_z = context.read_float()

        result._origin_x = context.read_float()
        result._origin_y = context.read_float()
        result._origin_z = context.read_float()

        result._data = context.read_float_array()

        return result
