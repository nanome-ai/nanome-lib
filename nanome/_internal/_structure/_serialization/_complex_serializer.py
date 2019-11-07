from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _StringSerializer
from nanome._internal._util._serializers import _Vector3Serializer, _QuaternionSerializer, _UnityPositionSerializer, _UnityRotationSerializer
from . import _MoleculeSerializer
from .. import _Complex

from nanome._internal._util._serializers import _TypeSerializer
from nanome.util import Quaternion, Vector3


class _ComplexSerializer(_TypeSerializer):
    def __init__(self, shallow=False):
        self.shallow = shallow
        self.array = _ArraySerializer()
        self.array.set_type(_MoleculeSerializer())
        self.string = _StringSerializer()

        self.dictionary = _DictionarySerializer()
        self.dictionary.set_types(self.string, self.string)

        self.vector = _Vector3Serializer()
        self.quaternion = _QuaternionSerializer()
        self.pos = _UnityPositionSerializer()
        self.rot = _UnityRotationSerializer()

    def version(self):
        return 3

    def name(self):
        return "Complex"

    def serialize(self, version, value, context):
        context.write_long(value._index)
        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._molecules)
        context.write_bool(value._boxed)
        context.write_bool(value._locked)
        context.write_bool(value._visible)
        context.write_bool(value._computing)
        context.write_int(value._current_frame)

        context.write_using_serializer(self.string, value._name)
        if version >= 2:
            context.write_int(value._index_tag)
            context.write_using_serializer(self.string, value._split_tag)
        if version >=3:
            context.write_using_serializer(self.pos, value._position)
            context.write_using_serializer(self.rot, value._rotation)
        else:
            position = Vector3._get_inversed_handedness(value._position)
            context.write_using_serializer(self.vector, position)
            rotation = Quaternion._get_inversed_handedness(value._rotation)
            context.write_using_serializer(self.quaternion, rotation)
        context.write_using_serializer(self.dictionary, value._remarks)

        #writing junk because selected flag is one directional.
        context.write_bool(False)
        context.write_bool(value._surface_dirty)
        context.write_float(value._surface_refresh_rate)

        if version >= 1:
            context.write_using_serializer(self.string, value._box_label)


    def deserialize(self, version, context):
        complex = _Complex._create()
        complex._index = context.read_long()

        complex._set_molecules(context.read_using_serializer(self.array))

        complex._boxed = context.read_bool()
        complex._locked = context.read_bool()
        complex._visible = context.read_bool()
        complex._computing = context.read_bool()
        complex._current_frame = context.read_int()

        complex._name = context.read_using_serializer(self.string)
        if version >= 2:
            complex._index_tag = context.read_int()
            complex._split_tag = context.read_using_serializer(self.string)
        if version >=3:
            complex._position = context.read_using_serializer(self.vector)
            complex._rotation = context.read_using_serializer(self.quaternion)
        else:
            complex._position = context.read_using_serializer(self.vector)._inverse_handedness()
            complex._rotation = context.read_using_serializer(self.quaternion)._inverse_handedness()

        complex._remarks = context.read_using_serializer(self.dictionary)
        #true iff at least 1 atom is selected in current molecule
        complex._selected = context.read_bool()
        context.read_bool()  # Read surface dirty but ignore it
        complex._surface_dirty = False
        complex._surface_refresh_rate = context.read_float()

        if version >= 1:
            complex._box_label = context.read_using_serializer(self.string)

        return complex
