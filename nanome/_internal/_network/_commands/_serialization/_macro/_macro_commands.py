from nanome._internal._util._serializers import _TypeSerializer, _ArraySerializer, _StringSerializer
from nanome._internal._macro._serialization import _MacroSerializer

macro_serializer = _MacroSerializer()
string_serializer = _StringSerializer()
class _SaveMacro(_TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer
    
    def __init__(self):
        pass

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

class _DeleteMacro(_TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        pass

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

class _RunMacro(_TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        pass

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


class _GetMacros(_TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "GetMacros"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._string_serializer, value)

    def deserialize(self, version, context):
        raise NotImplementedError

class _GetMacrosResponse(_TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        self._array_serializer = _ArraySerializer()
        self._array_serializer.set_type(self._macro_serializer)

    def version(self):
        return 0

    def name(self):
        return "GetMacrosResponse"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return context.read_using_serializer(self._array_serializer)

class _StopMacro(_TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "StopMacro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._string_serializer, value)

    def deserialize(self, version, context):
        raise NotImplementedError