from nanome._internal._util._serializers import _TypeSerializer, _UnityPositionSerializer, _UnityRotationSerializer


class _GetControllerTransformsResponse(_TypeSerializer):
    def __init__(self):
        self.pos = _UnityPositionSerializer()
        self.rot = _UnityRotationSerializer()

    def version(self):
        return 0

    def name(self):
        return "GetControllerTransformsResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        headset_position = context.read_using_serializer(self.pos)
        headset_rotation = context.read_using_serializer(self.rot)
        left_controller_position = context.read_using_serializer(self.pos)
        left_controller_rotation = context.read_using_serializer(self.rot)
        right_controller_position = context.read_using_serializer(self.pos)
        right_controller_rotation = context.read_using_serializer(self.rot)

        result = (headset_position, headset_rotation, left_controller_position, left_controller_rotation, right_controller_position, right_controller_rotation)
        return result
