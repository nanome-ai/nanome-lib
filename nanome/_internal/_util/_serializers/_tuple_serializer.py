from nanome._internal._util._serializers import _TypeSerializer


class _TupleSerializer(_TypeSerializer):
    def __init__(self, serializer1=None, serializer2=None):
        self._serializer1 = serializer1
        self._serializer2 = serializer2

    def version(self):
        return 0

    def name(self):
        return "Tuple"

    def serialize(self, version, value, context):
        if self._serializer1 == None or self._serializer2 == None:
            raise TypeError('Trying to serialize tuple without setting content type first')
        (first, second) = value
        context.write_using_serializer(self._serializer1, first)
        context.write_using_serializer(self._serializer2, second)

    def deserialize(self, version, context):
        if self._serializer1 == None or self._serializer2 == None:
            raise TypeError('Trying to deserialize tuple without setting content type first')
        first = context.read_using_serializer(self._serializer1)
        second = context.read_using_serializer(self._serializer2)
        return (first, second)

    def set_types(self, serializer1, serializer2):
        self._serializer1 = serializer1
        self._serializer2 = serializer2
