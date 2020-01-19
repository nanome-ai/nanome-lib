from nanome._internal._util._serializers import _TypeSerializer

class _ButtonCallback(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 2

    def name(self):
        return "ButtonCallback"
        
    def serialize(self, version, value, context):
        id = value[0]
        state = value[1]
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            id |= plugin_mask
        context.write_int(id)
        if version >= 2:
            context.write_bool(state)

    def deserialize(self, version, context):
        content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            content_id &= id_mask
        state = False
        if version >= 2:
            state = context.read_bool()
        return (content_id, state)
