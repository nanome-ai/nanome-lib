from nanome._internal._util._serializers import _TypeSerializer

class _MenuCallback(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "MenuCallback"
        
    def serialize(self, version, value, context):
        if version >= 1:
            context.write_byte(value[0])
        context.write_bool(value[1])

    def deserialize(self, version, context):
        if version >= 1:
            index = context.read_byte()
        else:
            index = 0
        value = context.read_bool()
        return (index, value)
