from nanome._internal._util._serializers import _TypeSerializer


class _ArraySerializer(_TypeSerializer):
    def __init__(self):
        self._serializer = None

    def version(self):
        return 0

    def name(self):
        return "Array"

    def serialize(self, version, value, context):
        if self._serializer == None:
            raise TypeError('Trying to serialize array without setting content type first')

        context.write_uint(len(value))
        for cur in value:
            context.write_using_serializer(self._serializer, cur)

    def deserialize(self, version, context):
        if self._serializer == None:
            raise TypeError('Trying to deserialize array without setting content type first')

        length = context.read_uint()
        result = []
        for _ in range(length):
            deserialized = context.read_using_serializer(self._serializer)
            result.append(deserialized)
        return result

    def set_type(self, serializer):
        self._serializer = serializer
