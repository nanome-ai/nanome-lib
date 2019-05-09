from nanome._internal._util._serializers import _TypeSerializer
from nanome._internal._user._serialization import _ControllerSerializer

class _ControllerRequest(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "ControllerRequest"

    def serialize(self, version, value, context):
        context.write_int(value)

    def deserialize(self, version, data):
        return None

class _ControllerResponse(_TypeSerializer):
    def __init__(self):
        self.controller_serializer = _ControllerSerializer()

    def version(self):
        return 0

    def name(self):
        return "ControllerResponse"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        result = context.read_using_serializer(self.controller_serializer)
        return result