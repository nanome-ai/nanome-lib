from nanome._internal import serializer_fields as fields
from . import serializers


class AddToWorkspace(fields.TypeSerializer):

    def __init__(self):
        self.__array = fields.ArraySerializer()
        self.__array.set_type(serializers.ComplexSerializer())
        atom_serializer = serializers.AtomSerializer()
        long_serializer = fields.LongSerializer()
        self.dict = fields.DictionarySerializer()
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


class ComplexAddedRemoved(fields.TypeSerializer):

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


class ComplexUpdated(fields.TypeSerializer):

    def __init__(self):
        self.complex_serializer = serializers.ComplexSerializer()
        atom_serializer = serializers.AtomSerializer()
        long_serializer = fields.LongSerializer()
        self.dict = fields.DictionarySerializer()
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


class ComplexUpdatedHook(fields.TypeSerializer):

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


class ComputeHBonds(fields.TypeSerializer):

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


class PositionStructures(fields.TypeSerializer):

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
            if isinstance(val, structure.models._Atom):
                atom_ids.append(val._index)
            elif isinstance(val, structure.models._Bond):
                atom_ids.append(val._atom1._index)
                atom_ids.append(val._atom2._index)
            # all other base objects implement the atoms generator
            elif isinstance(val, structure.models._Base):
                for atom in val.atoms:
                    atom_ids.append(atom._index)

        context.write_long_array(atom_ids)

    def deserialize(self, version, context):
        return None


class PositionStructuresDone(fields.TypeSerializer):

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


class ReceiveComplexList(fields.TypeSerializer):

    def __init__(self):
        self.array_serializer = fields.ArraySerializer()
        self.array_serializer.set_type(serializers.ComplexSerializer())

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


class ReceiveComplexes(fields.TypeSerializer):

    def __init__(self):
        self.array_serializer = fields.ArraySerializer()
        self.array_serializer.set_type(serializers.ComplexSerializer())
        atom_serializer = serializers.AtomSerializer()
        long_serializer = fields.LongSerializer()
        self.dict = fields.DictionarySerializer()
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


class ReceiveWorkspace(fields.TypeSerializer):

    def __init__(self):
        self.workspace = serializers.WorkspaceSerializer()
        atom_serializer = serializers.AtomSerializer()
        long_serializer = fields.LongSerializer()
        self.dict = fields.DictionarySerializer()
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


class RequestComplexList(fields.TypeSerializer):

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


class RequestComplexes(fields.TypeSerializer):

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


class RequestSubstructure(fields.TypeSerializer):

    def __init__(self):
        self.array = fields.ArraySerializer()
        self.array.set_type(serializers.SubstructureSerializer())
        self.dict = fields.DictionarySerializer()
        self.dict.set_types(fields.LongSerializer(), serializers.AtomSerializer())
        self.molecule = serializers.MoleculeSerializer()

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


class RequestWorkspace(fields.TypeSerializer):

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


class SelectionChanged(fields.TypeSerializer):

    def __init__(self):
        self.complex_serializer = serializers.ComplexSerializer()
        atom_serializer = serializers.AtomSerializer()
        long_serializer = fields.LongSerializer()
        self.dict = fields.DictionarySerializer()
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


class SelectionChangedHook(fields.TypeSerializer):

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


class UpdateStructures(fields.TypeSerializer):
    def __init__(self, shallow):
        self.array_serializer = fields.ArraySerializer()
        # setting the shallow flag
        self.complex_serializer = serializers.ComplexSerializer(shallow)
        self.molecule_serializer = serializers.MoleculeSerializer(shallow)
        self.chain_serializer = serializers.ChainSerializer(shallow)
        self.residue_serializer = serializers.ResidueSerializer(shallow)
        self.bond_serializer = serializers.BondSerializer(shallow)
        self.atom_serializer = serializers.AtomSerializerID(shallow)
        # atom dict only used by deep
        self.dict = fields.DictionarySerializer()
        self.dict.set_types(fields.LongSerializer(), serializers.AtomSerializer())

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
            if isinstance(val, structure.models._Atom):
                atoms.append(val)
            if isinstance(val, structure.models._Bond):
                bonds.append(val)
            if isinstance(val, structure.models._Residue):
                residues.append(val)
            if isinstance(val, structure.models._Chain):
                chains.append(val)
            if isinstance(val, structure.models._Molecule):
                molecules.append(val)
            if isinstance(val, structure.models._Complex):
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


class UpdateStructuresDeepDone(fields.TypeSerializer):

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


class UpdateWorkspace(fields.TypeSerializer):

    def __init__(self):
        self.workspace = serializers.WorkspaceSerializer()
        atom_serializer = serializers.AtomSerializer()
        long_serializer = fields.LongSerializer()
        self.dict = fields.DictionarySerializer()
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


class AddBonds(fields.TypeSerializer):

    def __init__(self):
        self.__array = fields.ArraySerializer()
        self.__array.set_type(serializers.ComplexSerializer())
        self.__dict = fields.DictionarySerializer()
        self.__dict.set_types(fields.LongSerializer(), serializers.AtomSerializer())

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


class AddDSSP(fields.TypeSerializer):

    def __init__(self):
        self.__array = fields.ArraySerializer()
        self.__array.set_type(serializers.ComplexSerializer())
        self.__dict = fields.DictionarySerializer()
        self.__dict.set_types(fields.LongSerializer(), serializers.AtomSerializer())

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
