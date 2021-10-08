from nanome._internal._network._serialization import _ContextDeserialization, _ContextSerialization
from nanome._internal._util._serializers import _TypeSerializer


class _SetSkybox(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "SetSkybox"

    def serialize(self, version, value, context):
        context.write_int(value)

    def deserialize(self, version, context):
        raise NotImplementedError
