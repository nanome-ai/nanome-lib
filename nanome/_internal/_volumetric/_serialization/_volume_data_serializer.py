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

        #reading as float so we divide length by 4
        context.write_uint(int(len(value._data)/4))
        context.write_bytes(value._data)

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

        #was written as float so we multiply length by 4
        length = context.read_uint()*4
        result._data = context.read_bytes(length)

        return result
