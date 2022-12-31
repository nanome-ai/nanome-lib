from nanome._internal._util._serializers import _TypeSerializer


class _SliderCallback(_TypeSerializer):
    def version(self):
        return 1

    def name(self):
        return "SliderCallback"

    def serialize(self, version, value, context):
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            value[0] |= plugin_mask
        context.write_int(value[0])
        context.write_float(value[1])

    def deserialize(self, version, context):
        content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            content_id &= id_mask
        result = (content_id, context.read_float())
        return result
