from nanome._internal.util.serializers import TypeSerializer, _DictionarySerializer, _StringSerializer, _ByteSerializer


class _AdvancedSettings(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "AdvancedSettings"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class _Connect(TypeSerializer):
    def __init__(self):
        self.__dictionary = _DictionarySerializer()
        self.__dictionary.set_types(_StringSerializer(), _ByteSerializer())

    def version(self):
        return 0

    def name(self):
        return "Connect"

    def serialize(self, version, value, data):
        data.write_byte(value[0])
        data.write_using_serializer(self.__dictionary, value[1])

    def deserialize(self, version, data):
        version_table = data.read_using_serializer(self.__dictionary)
        return version_table


class _Run(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "Run"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


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
