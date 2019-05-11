from nanome._internal._util._serializers import _TypeSerializer
from nanome._internal._user._serialization import _ControllerSerializer

class _ControllerHook(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "ControllerHook"

    def serialize(self, version, value, context):
        #value is a tuple of the form:
        #controller_type, controller_button, controller_event
        context.write_uint(value[0])
        context.write_uint(value[1])
        context.write_uint(value[2])

    def deserialize(self, version, data):
        return None

class _ControllerUnhook(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "ControllerUnhook"

    def serialize(self, version, value, context):
        #value is a tuple of the form:
        #controller_type, controller_button, controller_event
        context.write_uint(value[0])
        context.write_uint(value[1])
        context.write_uint(value[2])

    def deserialize(self, version, data):
        return None


class _ControllerCallback(_TypeSerializer):
    def __init__(self):
        self.controller_serializer = _ControllerSerializer()

    def version(self):
        return 0

    def name(self):
        return "ControllerCallback"

    def serialize(self, version, value, context):
        #value is a tuple of the form:
        #controller_type, controller_button, controller_event, controller
        context.write_uint(value[0])
        context.write_uint(value[1])
        context.write_uint(value[2])
        context.write_using_serializer(_ControllerSerializer, value[3])

    def deserialize(self, version, context):
        controller_type = context.read_uint()
        controller_button = context.read_uint()
        controller_event = context.read_uint()
        controller = context.read_using_serializer(self.controller_serializer)
        return (controller_type, controller_button, controller_event, controller)