from nanome._internal.util.serializers import TypeSerializer


class _UpdateStructuresDeepDone(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "UpdateStructureDeepDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None
