from nanome._internal._network._serialization import _ContextDeserialization, _ContextSerialization
from nanome._internal._util._serializers import _DictionarySerializer, _LongSerializer
from nanome._internal._structure._serialization import _WorkspaceSerializer, _AtomSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _UpdateWorkspace(_TypeSerializer):
    def __init__(self):
        self.workspace = _WorkspaceSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = _LongSerializer()
        self.dict = _DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "UpdateWorkspace"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.workspace, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        raise NotImplementedError