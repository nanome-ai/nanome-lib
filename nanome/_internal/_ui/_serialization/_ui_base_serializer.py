from nanome.util import Logs, IntEnum

from nanome._internal._util._serializers import _TypeSerializer


class _UIBaseSerializer(_TypeSerializer):
    class ContentType(IntEnum):
        ebutton = 0
        emesh = 1
        eslider = 2
        etextInput = 3
        elabel = 4
        elist = 5
        eimage = 6
        eloadingBar = 7
        edropdown = 8

    registered_classes = dict()
    registered_serializers = dict()

    @classmethod
    def register_type(cls, classname, enum_value, serializer):
        cls.registered_classes[classname] = enum_value
        cls.registered_serializers[enum_value] = serializer

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "UIContent"

    def serialize(self, version, value, context):
        if value == None:
            return
        try:
            ui_type = _UIBaseSerializer.registered_classes[type(value).__name__]
            serializer = _UIBaseSerializer.registered_serializers[ui_type]
        except:
            Logs.error("Trying to serialize unknown UI type:", type(value).__name__)
            return
        context.write_uint(ui_type)
        context.write_using_serializer(serializer, value)

    def deserialize(self, version, context):
        ui_type = _UIBaseSerializer.ContentType(context.read_uint())
        try:
            serializer = _UIBaseSerializer.registered_serializers[ui_type]
        except:
            Logs.error("Trying to deserialize unknown UI type:", ui_type)
            return
        return context.read_using_serializer(serializer)
