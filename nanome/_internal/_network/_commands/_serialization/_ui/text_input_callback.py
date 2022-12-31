from nanome._internal._util._serializers import _TypeSerializer, _TupleSerializer, _IntSerializer, _StringSerializer


class _TextInputCallback(_TypeSerializer):
    def __init__(self):
        self.__tuple = _TupleSerializer(_IntSerializer(), _StringSerializer())

    def version(self):
        return 1

    def name(self):
        return "TextInputCallback"

    def serialize(self, version, value, context):
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            value[0] |= plugin_mask
        context.write_using_serializer(self.__tuple, value)

    def deserialize(self, version, context):
        tup = context.read_using_serializer(self.__tuple)
        if (version == 0):
            id_mask = 0x00FFFFFF
            tup = (tup[0] & id_mask, tup[1])
        return tup
