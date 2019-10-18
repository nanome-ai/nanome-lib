from nanome._internal._util._serializers import _TypeSerializer, _Vector3Serializer, _QuaternionSerializer


class _GetMenuTransformResponse(_TypeSerializer):
    def __init__(self):
        self.vector = _Vector3Serializer()
        self.quat = _QuaternionSerializer()

    def version(self):
        return 0

    def name(self):
        return "GetMenuTransformResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        menu_position = context.read_using_serializer(self.vector)
        menu_rotation = context.read_using_serializer(self.quat)

        result = (menu_position, menu_rotation)
        return result
