from nanome._internal import serializer_fields


class AdvancedSettings(serializer_fields.TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "AdvancedSettings"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class Connect(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__dictionary = serializer_fields.DictionaryField()
        self.__dictionary.set_types(serializer_fields.StringField(), serializer_fields.ByteField())

    def version(self):
        return 0

    def name(self):
        return "Connect"

    def serialize(self, version, value, data):
        data.write_byte(value[0])
        data.write_using_serializer(self.__dictionary, value[1])

    def deserialize(self, version, data):
        version_table = data.read_using_serializer(self.__dictionary)
        return version_table


class Run(serializer_fields.TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "Run"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class SetPluginListButton(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "SetPluginListButton"

    def serialize(self, version, value, data):
        data.write_uint(value[0])
        data.write_using_serializer(self.__string, value[1])
        data.write_bool(value[2])

    def deserialize(self, version, data):
        return None


class OpenURL(serializer_fields.TypeSerializer):

    def __init__(self):
        self.string = serializer_fields.StringField()

    def version(self):
        return 1

    def name(self):
        return "OpenURL"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value[0])  # URL
        if version >= 1:
            context.write_bool(value[1])  # Desktop Browser

    def deserialize(self, version, context):
        raise NotImplementedError


class GetControllerTransforms(serializer_fields.TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "GetControllerTransforms"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class GetControllerTransformsResponse(serializer_fields.TypeSerializer):

    def __init__(self):
        self.pos = serializer_fields.UnityPositionField()
        self.rot = serializer_fields.UnityRotationField()

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

        result = (headset_position, headset_rotation, left_controller_position,
                  left_controller_rotation, right_controller_position, right_controller_rotation)
        return result
