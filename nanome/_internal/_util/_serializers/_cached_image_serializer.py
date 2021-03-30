from . import _StringSerializer
from nanome._internal._util._serializers import _TypeSerializer

class _CachedImageSerializer(_TypeSerializer):
    Cache = set()
    def __init__(self):
        self._string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "CachedImage"

    def serialize(self, version, value, context):
        if value == None or value == "":
            context.write_bool(False)
            context.write_using_serializer(self._string, "")
            context.write_byte_array([])
            return

        if value in _CachedImageSerializer.Cache:
            context.write_bool(True)
            context.write_using_serializer(self._string, value)
        else:
            with open(value, "rb") as f:
                data = f.read()
            context.write_bool(False)
            context.write_using_serializer(self._string, value)
            context.write_byte_array(data)
            _CachedImageSerializer.Cache.add(value)

    def deserialize(self, version, context):
        raise NotImplementedError
