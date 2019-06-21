from nanome._internal._util._serializers import _TypeSerializer

class _ButtonCallback(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "ButtonCallback"
        
    def serialize(self, version, value, context):
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            value |= plugin_mask
        context.write_int(value)

    def deserialize(self, version, context):
        content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            content_id &= id_mask
        return content_id
