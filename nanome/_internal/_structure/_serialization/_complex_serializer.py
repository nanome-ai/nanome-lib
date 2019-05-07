from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _StringSerializer, _Vector3Serializer, _QuaternionSerializer
from . import _MoleculeSerializer
from .. import _Complex

from nanome._internal._util._serializers import _TypeSerializer


class _ComplexSerializer(_TypeSerializer):
    def __init__(self, shallow=False):
        self.shallow = shallow
        self.array = _ArraySerializer()
        self.array.set_type(_MoleculeSerializer())
        self.string = _StringSerializer()
        self.vector = _Vector3Serializer()
        self.quaternion = _QuaternionSerializer()
        self.dictionary = _DictionarySerializer()
        self.dictionary.set_types(self.string, self.string)

    def version(self):
        return 0

    def name(self):
        return "Complex"

    def serialize(self, version, value, context):
        context.write_long(value._index)
        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._molecules)
        context.write_bool(value._rendering._boxed)
        context.write_bool(value._rendering._visible)
        context.write_bool(value._rendering._computing)
        context.write_int(value._rendering._current_frame)

        context.write_using_serializer(self.string, value._molecular._name)
        context.write_using_serializer(self.vector, value._transform._position)
        context.write_using_serializer(self.quaternion, value._transform._rotation)

        context.write_using_serializer(
            self.dictionary, value._molecular._remarks)

    def deserialize(self, version, context):
        complex = _Complex._create()
        complex._index = context.read_long()

        complex._molecules = context.read_using_serializer(self.array)
        complex._rendering._boxed = context.read_bool()
        complex._rendering._visible = context.read_bool()
        complex._rendering._computing = context.read_bool()
        complex._rendering._current_frame = context.read_int()

        complex._molecular._name = context.read_using_serializer(self.string)
        complex._transform._position = context.read_using_serializer(
            self.vector)
        complex._transform._rotation = context.read_using_serializer(
            self.quaternion)

        complex._molecular._remarks = context.read_using_serializer(
            self.dictionary)
        return complex
