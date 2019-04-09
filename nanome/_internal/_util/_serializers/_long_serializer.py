from nanome._internal._util._serializers import _TypeSerializer

class _LongSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "long"
        
    def serialize(self, version, value, context):
        context.write_long(value)

    def deserialize(self, version, context):
        return context.read_long()