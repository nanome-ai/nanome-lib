from .. import _VolumeData
from nanome._internal._util._serializers import _TypeSerializer

class _UnitCellSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "UnitCell"

    def serialize(self, version, value, context):
        context.write_float(value._A)
        context.write_float(value._B)
        context.write_float(value._C)
        context.write_float(value._Alpha)
        context.write_float(value._Beta)
        context.write_float(value._Gamma)
        context.write_float(value._Origin.x)
        context.write_float(value._Origin.y)
        context.write_float(value._Origin.z)

    def deserialize(self, version, context):
        raise NotImplementedError
