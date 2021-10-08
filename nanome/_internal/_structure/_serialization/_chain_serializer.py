from nanome._internal._util._serializers import _ArraySerializer, _StringSerializer
from . import _ResidueSerializer
from .. import _Chain

from nanome._internal._util._serializers import _TypeSerializer


class _ChainSerializer(_TypeSerializer):
    def __init__(self, shallow=False):
        self.shallow = shallow
        self.array_serializer = _ArraySerializer()
        self.array_serializer.set_type(_ResidueSerializer())
        self.string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "Chain"

    def serialize(self, version, value, context):
        context.write_long(value._index)
        if (self.shallow):
            context.write_using_serializer(self.array_serializer, [])
        else:
            context.write_using_serializer(self.array_serializer, value._residues)
        context.write_using_serializer(self.string, value._name)

    def deserialize(self, version, context):
        chain = _Chain._create()
        chain._index = context.read_long()

        chain._set_residues(context.read_using_serializer(self.array_serializer))
        chain._name = context.read_using_serializer(self.string)
        return chain
