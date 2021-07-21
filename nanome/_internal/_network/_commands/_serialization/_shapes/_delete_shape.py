from nanome._internal._util._serializers import _TypeSerializer
from nanome.util.logs import Logs


class _DeleteShape(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "DeleteShape"

    def serialize(self, version, value, context):
        if version == 0:
            if len(value) > 1:
                msg = "SetShape: Using a list of shapes with an old version of Nanome"
                Logs.warning(msg)
                raise TypeError(msg)
            context.write_int(value[0])
        elif version == 1:
            context.write_int_array(value)

    def deserialize(self, version, context):
        if version == 0:
            return [context.read_bool()]
        elif version == 1:
            return context.read_byte_array()
