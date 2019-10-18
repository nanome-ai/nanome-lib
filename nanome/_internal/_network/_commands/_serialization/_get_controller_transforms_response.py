from nanome._internal._util._serializers import _TypeSerializer, _Vector3Serializer, _QuaternionSerializer


class _GetControllerTransformsResponse(_TypeSerializer):
    def __init__(self):
        self.vector = _Vector3Serializer()
        self.quat = _QuaternionSerializer()

    def version(self):
        return 0

    def name(self):
        return "GetControllerTransformsResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        headset_position = context.read_using_serializer(self.vector)
        headset_rotation = context.read_using_serializer(self.quat)
        left_controller_position = context.read_using_serializer(self.vector)
        left_controller_rotation = context.read_using_serializer(self.quat)
        right_controller_position = context.read_using_serializer(self.vector)
        right_controller_rotation = context.read_using_serializer(self.quat)

        result = (headset_position, headset_rotation, left_controller_position, left_controller_rotation, right_controller_position, right_controller_rotation)
        return result
