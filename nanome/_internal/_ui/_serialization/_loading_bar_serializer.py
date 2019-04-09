from enum import IntEnum
from . import _UIBaseSerializer
from .. import _LoadingBar
from nanome._internal._util._serializers import _StringSerializer, _TypeSerializer

class _LoadingBarSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "LoadingBar"

    def serialize(self, version, value, context):
        context.write_int(value._content_id)
        context.write_float(value._percentage)
        context.write_using_serializer(self.string, value._title)
        context.write_using_serializer(self.string, value._description)
        context.write_bool(value._failure)

    def deserialize(self, version, context):
        value = _LoadingBar._create()
        value._content_id = context.read_int()
        value._percentage = context.read_float()
        value._title = context.read_using_serializer(self.string)
        value._description = context.read_using_serializer(self.string)
        value._failure = context.read_bool()
        return value

_UIBaseSerializer.register_type("LoadingBar", _UIBaseSerializer.ContentType.eloadingBar, _LoadingBarSerializer())
