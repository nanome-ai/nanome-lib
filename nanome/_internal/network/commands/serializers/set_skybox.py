from nanome._internal.network.serialization import _ContextDeserialization, _ContextSerialization
from nanome._internal.util.serializers import TypeSerializer


class _SetSkybox(TypeSerializer):
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
