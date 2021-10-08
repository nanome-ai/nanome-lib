from . import _TupleSerializer, _ArraySerializer

from nanome._internal._util._serializers import _TypeSerializer


class _DictionarySerializer(_TypeSerializer):
    def __init__(self):
        self._serializer = None

    def version(self):
        return 0

    def name(self):
        return "Dictionary"

    def serialize(self, version, value, context):
        if self._serializer == None:
            raise TypeError('Trying to serialize dictionary without setting content type first')
        context.write_using_serializer(self._serializer, value.items())

    def deserialize(self, version, context):
        if self._serializer == None:
            raise TypeError('Trying to deserialize dictionary without setting content type first')
        result = dict(context.read_using_serializer(self._serializer))
        return result

    def set_types(self, serializer1, serializer2):
        tuple_serializer = _TupleSerializer()
        tuple_serializer.set_types(serializer1, serializer2)
        self._serializer = _ArraySerializer()
        self._serializer.set_type(tuple_serializer)
