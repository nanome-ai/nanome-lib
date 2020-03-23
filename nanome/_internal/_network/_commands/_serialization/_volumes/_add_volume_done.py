from nanome._internal._util._serializers import _TypeSerializer

class _AddVolumeDone(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "AddVolumeDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None