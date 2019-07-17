from nanome._internal._util._serializers import _TypeSerializer
from nanome._internal._macro._serialization import _MacroSerializer

macro_serializer = _MacroSerializer()

class _SaveMacro(_TypeSerializer):
    def __init__(self):
        self._macro_serializer = macro_serializer

    def version(self):
        return 0

    def name(self):
        return "SaveMacro"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None