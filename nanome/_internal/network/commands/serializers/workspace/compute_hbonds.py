from nanome._internal.network.serialization import _ContextDeserialization, _ContextSerialization
from nanome._internal.util.serializers import TypeSerializer


class _ComputeHBonds(TypeSerializer):
    def __init__(self):
        pass

    def name(self):
        return "ComputeHBonds"

    def version(self):
        return 0

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return None
