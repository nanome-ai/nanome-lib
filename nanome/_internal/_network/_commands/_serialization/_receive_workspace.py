from nanome._internal._structure._serialization import _WorkspaceSerializer, _AtomSerializer
from nanome._internal._util._serializers import _DictionarySerializer, _LongSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _ReceiveWorkspace(_TypeSerializer):
    def __init__(self):
        self.workspace = _WorkspaceSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = _LongSerializer()
        self.dict = _DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "ReceiveWorkspace"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        workspace = context.read_using_serializer(self.workspace)
        return workspace