from nanome._internal._structure import _Atom, _Bond, _Residue, _Chain, _Molecule, _Complex, _Base
from nanome._internal._network._serialization import _ContextDeserialization, _ContextSerialization
from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _LongSerializer, _TypeSerializer
from nanome._internal._structure._serialization import _ComplexSerializer, _MoleculeSerializer, _ChainSerializer, _ResidueSerializer, _BondSerializer, _AtomSerializer, _AtomSerializerID

# deep


class _UpdateStructures(_TypeSerializer):
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
