from . import serializers
from nanome._internal import serializer_fields

macro_serializer = serializers.MacroSerializer()
string_serializer = serializer_fields.StringField()


class SaveMacro(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def version(self):
        return 0

    def name(self):
        return "SaveMacro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._macro_serializer, value[0])
        context.write_bool(value[1])
        context.write_using_serializer(self._string_serializer, value[2])

    def deserialize(self, version, context):
        raise NotImplementedError


class DeleteMacro(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def version(self):
        return 0

    def name(self):
        return "DeleteMacro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._macro_serializer, value[0])
        context.write_bool(value[1])
        context.write_using_serializer(self._string_serializer, value[2])

    def deserialize(self, version, context):
        raise NotImplementedError


class RunMacro(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def version(self):
        return 1

    def name(self):
        return "RunMacro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._macro_serializer, value)

    def deserialize(self, version, context):
        if version < 1:
            return
        return context.read_bool()


class GetMacros(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def version(self):
        return 0

    def name(self):
        return "GetMacros"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._string_serializer, value)

    def deserialize(self, version, context):
        raise NotImplementedError


class GetMacrosResponse(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        self._array_serializer = serializer_fields.ArrayField()
        self._array_serializer.set_type(self._macro_serializer)

    def version(self):
        return 0

    def name(self):
        return "GetMacrosResponse"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return context.read_using_serializer(self._array_serializer)


class StopMacro(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def version(self):
        return 0

    def name(self):
        return "StopMacro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._string_serializer, value)

    def deserialize(self, version, context):
        raise NotImplementedError
