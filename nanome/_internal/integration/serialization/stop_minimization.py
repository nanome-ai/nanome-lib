from nanome._internal.util.type_serializers import TypeSerializer


class _StopMinimization(TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "StopMinimization"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return None
