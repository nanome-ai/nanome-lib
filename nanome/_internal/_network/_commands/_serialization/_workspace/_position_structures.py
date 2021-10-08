from nanome._internal._structure import _Atom, _Bond, _Residue, _Chain, _Molecule, _Complex, _Base
from nanome._internal._network._serialization import _ContextDeserialization, _ContextSerialization
from nanome._internal._util._serializers import _ArraySerializer, _TypeSerializer, _LongSerializer
# from nanome._internal._structure._serialization import _Long
import types

# deep


class _PositionStructures(_TypeSerializer):
    def __init__(self):
        pass

    def name(self):
        return "PositionStructures"

    def version(self):
        return 0

    def serialize(self, version, value, context):
        # value is a structure[]
        if not isinstance(value, list) and not isinstance(value, types.GeneratorType):
            value = [value]

        atom_ids = []

        for val in value:
            if isinstance(val, _Atom):
                atom_ids.append(val._index)
            elif isinstance(val, _Bond):
                atom_ids.append(val._atom1._index)
                atom_ids.append(val._atom2._index)
            # all other base objects implement the atoms generator
            elif isinstance(val, _Base):
                for atom in val.atoms:
                    atom_ids.append(atom._index)

        context.write_long_array(atom_ids)

    def deserialize(self, version, context):
        return None
