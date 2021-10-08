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


class _RequestComplexes(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "RequestComplexes"

    def serialize(self, version, value, context):
        context.write_long_array(value)

    def deserialize(self, version, context):
        return None
