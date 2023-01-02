from nanome._internal.util.serializers import _StringSerializer, TypeSerializer


class _SetPluginListButton(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "SetPluginListButton"

    def serialize(self, version, value, data):
        data.write_uint(value[0])
        data.write_using_serializer(self.__string, value[1])
        data.write_bool(value[2])

    def deserialize(self, version, data):
        return None
