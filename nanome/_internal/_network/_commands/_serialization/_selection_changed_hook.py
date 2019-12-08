from nanome._internal._util._serializers import _TypeSerializer

class _SelectionChangedHook(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "SelectionChangedHook"

    def serialize(self, version, value, context):
        context.write_long(value)

    def deserialize(self, version, context):
        raise NotImplementedError
