from nanome._internal._util._serializers import _TypeSerializer
from nanome._internal._util._serializers import _Vector3Serializer
from nanome._internal._user import _Controller

class _ControllerSerializer (_TypeSerializer):
    def __init__(self):
        self.vector3_serializer = _Vector3Serializer()

    def version(self):
        return 0

    def name(self):
        return "Controller"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        result = _Controller._create()
        controller_type = context.read_int()
        result._controller_type = _Controller._ControllerType(controller_type)
        result._position = context.read_using_serializer(self.vector3_serializer)
        result._rotation = context.read_using_serializer(self.vector3_serializer)
        result._thumb_padX = context.read_float()
        result._thumb_padY = context.read_float()
        result._trigger_position = context.read_bool()
        result._grip_position = context.read_bool()
        result._button1_pressed = context.read_bool()
        result._button2_pressed = context.read_bool()
        return result