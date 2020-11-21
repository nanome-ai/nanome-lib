from nanome._internal._util._serializers import _TypeSerializer

class _BytesArraySerializer(_TypeSerializer):
    def __init__(self):
        self._serializer = None

    def version(self):
        return 0

    def name(self):
        return "BytesArray"
        
    def serialize(self, version, value, context):
        context.write_uint(len(value))
        context.write_bytes(value)

    def deserialize(self, version, context):
        length = context.read_uint()
        result = context.read_bytes(length)
        return result

    def set_type(self, serializer):
        self._serializer = serializer
