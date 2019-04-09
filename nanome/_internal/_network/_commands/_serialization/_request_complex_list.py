from nanome._internal._util._serializers import _ArraySerializer, _LongSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _RequestComplexList(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "RequestComplexList"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return None

from nanome._internal._util._serializers import _TypeSerializer

class _RequestComplexes(_TypeSerializer):
    def __init__(self):
        self._array = _ArraySerializer()
        self._array.set_type(_LongSerializer())

    def version(self):
        return 0

    def name(self):
        return "RequestComplexes"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._array, value)

    def deserialize(self, version, context):
        return None