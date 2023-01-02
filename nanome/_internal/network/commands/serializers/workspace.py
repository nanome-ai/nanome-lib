from nanome._internal.util.serializers import _ArraySerializer, _LongSerializer
from nanome._internal.structure.serialization import _WorkspaceSerializer, _AtomSerializer
from nanome._internal.structure import _Atom, _Bond, _Residue, _Chain, _Molecule, _Complex, _Base
from nanome._internal.network.serialization import ContextDeserialization, ContextSerialization
from nanome._internal.network.serialization import ContextSerialization
from nanome._internal.structure.serialization import _ComplexSerializer, _MoleculeSerializer, _ChainSerializer, _ResidueSerializer, _BondSerializer, _AtomSerializer, _AtomSerializerID
from nanome._internal.util.serializers import _ArraySerializer, _DictionarySerializer, _LongSerializer, TypeSerializer
from nanome._internal.structure.serialization import _SubstructureSerializer, _AtomSerializer, _MoleculeSerializer
from nanome._internal.util.serializers import _DictionarySerializer, _LongSerializer
import types
from nanome._internal.util.serializers import _ArraySerializer, TypeSerializer, _LongSerializer
from nanome._internal.util.serializers import TypeSerializer
from nanome._internal.util.serializers import _ArraySerializer, _DictionarySerializer, _LongSerializer
from nanome._internal.structure.serialization import _ComplexSerializer, _AtomSerializer
from nanome._internal.util.serializers import TypeSerializer, _ArraySerializer, _DictionarySerializer, _LongSerializer


class _AddBonds(TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_ComplexSerializer())
        self.__dict = _DictionarySerializer()
        self.__dict.set_types(_LongSerializer(), _AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "AddBonds"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}

        subcontext.write_using_serializer(self.__array, value)

        context.write_using_serializer(self.__dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.__dict)
        complexes = context.read_using_serializer(self.__array)
        return complexes


class _AddDSSP(TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_ComplexSerializer())
        self.__dict = _DictionarySerializer()
        self.__dict.set_types(_LongSerializer(), _AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "AddDSSP"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}

        subcontext.write_using_serializer(self.__array, value)

        context.write_using_serializer(self.__dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.__dict)
        complexes = context.read_using_serializer(self.__array)
        return complexes


class _AddToWorkspace(TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_ComplexSerializer())
        atom_serializer = _AtomSerializer()
        long_serializer = _LongSerializer()
        self.dict = _DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "AddToWorkspace"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.__array, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.__array)
        return complexes


class _ComplexAddedRemoved(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "ComplexAddedRemoved"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class _ComplexUpdated(TypeSerializer):
    def __init__(self):
        self.complex_serializer = _ComplexSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = _LongSerializer()
        self.dict = _DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "ComplexUpdated"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        index = context.read_long()
        has_complex = context.read_bool()

        if has_complex:
            context.payload["Atom"] = context.read_using_serializer(self.dict)
            complex = context.read_using_serializer(self.complex_serializer)
        else:
            complex = None
        return (index, complex)


class _ComplexUpdatedHook(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "ComplexUpdatedHook"

    def serialize(self, version, value, context):
        context.write_long(value)

    def deserialize(self, version, context):
        raise NotImplementedError


class _ComputeHBonds(TypeSerializer):
    def __init__(self):
        pass

    def name(self):
        return "ComputeHBonds"

    def version(self):
        return 0

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return None


# from nanome._internal.structure.serialization import _Long

# deep


class _PositionStructures(TypeSerializer):
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


class _PositionStructuresDone(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "PositionStructuresDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None


# shallow


class _ReceiveComplexList(TypeSerializer):
    def __init__(self):
        self.array_serializer = _ArraySerializer()
        self.array_serializer.set_type(_ComplexSerializer())

    def version(self):
        return 0

    def name(self):
        return "ReceiveComplexList"

    def serialize(self, version, value, context):
        raise NotImplementedError
        #context.write_using_serializer(self.array_serializer, value)

    def deserialize(self, version, data):
        complexes = data.read_using_serializer(self.array_serializer)

        return complexes

# deep


class _ReceiveComplexes(TypeSerializer):
    def __init__(self):
        self.array_serializer = _ArraySerializer()
        self.array_serializer.set_type(_ComplexSerializer())
        atom_serializer = _AtomSerializer()
        long_serializer = _LongSerializer()
        self.dict = _DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "ReceiveComplexes"

    def serialize(self, version, value, context):
        raise NotImplementedError
        #context.write_using_serializer(self.array_serializer, value)

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.array_serializer)
        return complexes


class _ReceiveWorkspace(TypeSerializer):
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


class _RequestComplexList(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "RequestComplexList"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return None


class _RequestComplexes(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "RequestComplexes"

    def serialize(self, version, value, context):
        context.write_long_array(value)

    def deserialize(self, version, context):
        return None


class _RequestSubstructure(TypeSerializer):
    def __init__(self):
        self.array = _ArraySerializer()
        self.array.set_type(_SubstructureSerializer())
        self.dict = _DictionarySerializer()
        self.dict.set_types(_LongSerializer(), _AtomSerializer())
        self.molecule = _MoleculeSerializer()

    def version(self):
        return 0

    def name(self):
        return "RequestSubstructure"

    def serialize(self, version, value, context):
        context.write_long(value[0])
        context.write_byte(int(value[1]))

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        molecule = context.read_using_serializer(self.molecule)
        substructures = context.read_using_serializer(self.array)

        residue_map = {}
        for chain in molecule.chains:
            for residue in chain.residues:
                residue_map[residue.index] = residue
        for substructure in substructures:
            substructure._residues = [residue_map[index]
                                      for index in substructure._residues]
        return substructures


class _RequestWorkspace(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "RequestWorkspace"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class _SelectionChanged(TypeSerializer):
    def __init__(self):
        self.complex_serializer = _ComplexSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = _LongSerializer()
        self.dict = _DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "SelectionChanged"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        index = context.read_long()
        has_complex = context.read_bool()

        if has_complex:
            context.payload["Atom"] = context.read_using_serializer(self.dict)
            complex = context.read_using_serializer(self.complex_serializer)
        else:
            complex = None
        return (index, complex)


class _SelectionChangedHook(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "SelectionChangedHook"

    def serialize(self, version, value, context):
        context.write_long(value)

    def deserialize(self, version, context):
        raise NotImplementedError


# deep


class _UpdateStructures(TypeSerializer):
    def __init__(self, shallow):
        self.array_serializer = _ArraySerializer()
        # setting the shallow flag
        self.complex_serializer = _ComplexSerializer(shallow)
        self.molecule_serializer = _MoleculeSerializer(shallow)
        self.chain_serializer = _ChainSerializer(shallow)
        self.residue_serializer = _ResidueSerializer(shallow)
        self.bond_serializer = _BondSerializer(shallow)
        self.atom_serializer = _AtomSerializerID(shallow)
        # atom dict only used by deep
        self.dict = _DictionarySerializer()
        self.dict.set_types(_LongSerializer(), _AtomSerializer())

    def name(self):
        return "UpdateStructures"

    def version(self):
        return 0

    def serialize(self, version, value, context):
        # value is a structure[]

        atoms = []
        bonds = []
        residues = []
        chains = []
        molecules = []
        complexes = []

        for val in value:
            if isinstance(val, _Atom):
                atoms.append(val)
            if isinstance(val, _Bond):
                bonds.append(val)
            if isinstance(val, _Residue):
                residues.append(val)
            if isinstance(val, _Chain):
                chains.append(val)
            if isinstance(val, _Molecule):
                molecules.append(val)
            if isinstance(val, _Complex):
                complexes.append(val)

        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}

        self.array_serializer.set_type(self.complex_serializer)
        subcontext.write_using_serializer(self.array_serializer, complexes)
        self.array_serializer.set_type(self.molecule_serializer)
        subcontext.write_using_serializer(self.array_serializer, molecules)
        self.array_serializer.set_type(self.chain_serializer)
        subcontext.write_using_serializer(self.array_serializer, chains)
        self.array_serializer.set_type(self.residue_serializer)
        subcontext.write_using_serializer(self.array_serializer, residues)
        self.array_serializer.set_type(self.bond_serializer)
        subcontext.write_using_serializer(self.array_serializer, bonds)
        self.array_serializer.set_type(self.atom_serializer)
        subcontext.write_using_serializer(self.array_serializer, atoms)

        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

        for complex in complexes:
            complex._surface_dirty = False

    def deserialize(self, version, context):
        return None


class _UpdateStructuresDeepDone(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "UpdateStructureDeepDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None


class _UpdateWorkspace(TypeSerializer):
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
