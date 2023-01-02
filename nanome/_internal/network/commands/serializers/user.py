from nanome._internal.util.serializers import TypeSerializer


class _GetControllerTransforms(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "GetControllerTransforms"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None
from nanome._internal.util.serializers import TypeSerializer, _UnityPositionSerializer, _UnityRotationSerializer


class _GetControllerTransformsResponse(TypeSerializer):
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
from nanome._internal.util.serializers import TypeSerializer


class _GetPresenterInfo(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "GetPresenterInfo"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None
from nanome._internal.util.serializers import TypeSerializer, _StringSerializer


class _GetPresenterInfoResponse(TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

    def version(self):
        return 1

    def name(self):
        return "GetPresenterInfoResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        from nanome.api.user import PresenterInfo

        result = PresenterInfo()
        result.account_id = context.read_using_serializer(self.string)
        result.account_name = context.read_using_serializer(self.string)
        result.account_email = context.read_using_serializer(self.string)
        result.has_org = context.read_bool()
        if result.has_org:
            result.org_id = context.read_int()
            result.org_name = context.read_using_serializer(self.string)

        return result
from nanome._internal.util.serializers import TypeSerializer


class _PresenterChange(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "PresenterChange"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None
