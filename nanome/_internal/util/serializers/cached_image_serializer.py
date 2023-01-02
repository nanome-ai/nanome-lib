from . import _StringSerializer
from nanome._internal.util.serializers import TypeSerializer


class CachedImageSerializer(TypeSerializer):
    cache = set()
    session = 0

    def __init__(self):
        self._string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "CachedImage"

    def serialize(self, version, value, context):
        session = CachedImageSerializer.session
        if value == None or value == "":
            context.write_bool(False)
            context.write_using_serializer(self._string, str(session) + "-")
            context.write_byte_array([])
            return

        if value in CachedImageSerializer.cache:
            context.write_bool(True)
            context.write_using_serializer(self._string, str(session) + "-" + value)
        else:
            with open(value, "rb") as f:
                data = f.read()
            context.write_bool(False)
            context.write_using_serializer(self._string, str(session) + "-" + value)
            context.write_byte_array(data)
            CachedImageSerializer.cache.add(value)

    def deserialize(self, version, context):
        # This function is only used by unit tests
        is_cached = context.read_bool()
        if is_cached:
            context.read_using_serializer(self._string)
        else:
            context.read_using_serializer(self._string)
            context.read_byte_array()
