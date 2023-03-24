from nanome._internal.serializer_fields import TypeSerializer, ArrayField, DictionaryField, LongField, ByteArrayField, LongField, StringField
from nanome._internal.enums import IntegrationCommands
from nanome.api._hashes import Hashes
from nanome.api.structure.serializers import ComplexSerializer, AtomSerializer

# In cases wher Hashes haven't been calculated yet, do so.
if all([hash == None for hash in Hashes.IntegrationHashes]):
    Hashes.init_hashes()


class AddHydrogenSerializer(TypeSerializer):
    def __init__(self):
        self.array_serializer = ArrayField()
        self.array_serializer.set_type(ComplexSerializer())
        atom_serializer = AtomSerializer()
        long_serializer = LongField()
        self.dict = DictionaryField()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "AddHydrogen"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.array_serializer, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.array_serializer)
        return complexes


class CalculateESPSerializer(TypeSerializer):
    def __init__(self):
        self.array_serializer = ArrayField()
        self.array_serializer.set_type(ComplexSerializer())
        atom_serializer = AtomSerializer()
        long_serializer = LongField()
        self.dict = DictionaryField()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "CalculateESP"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.array_serializer, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.array_serializer)
        return complexes


class ExportFileSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringField()

    def version(self):
        return 0

    def name(self):
        return "ExportFile"

    def serialize(self, version, value, context):
        context.write_bool(value)

    def deserialize(self, version, context):
        location = context.read_using_serializer(self.string)
        filename = context.read_using_serializer(self.string)
        data = context.read_byte_array()
        return (location, filename, data)


class ExportLocationsSerializer(TypeSerializer):
    def __init__(self):
        self.array = ArrayField()
        self.array.set_type(StringField())

    def version(self):
        return 0

    def name(self):
        return "ExportLocations"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.array, value)

    def deserialize(self, version, context):
        return None


class ExportSmilesSerializer(TypeSerializer):
    def __init__(self):
        self.complex_array = ArrayField()
        self.complex_array.set_type(ComplexSerializer())
        self.string_array = ArrayField()
        self.string_array.set_type(StringField())

        self.dict = DictionaryField()
        self.dict.set_types(LongField(), AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "ExportSmiles"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string_array, value)

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.complex_array)
        return complexes


class GenerateMoleculeImageSerializer(TypeSerializer):
    def __init__(self):
        self.complex_array = ArrayField()
        self.complex_array.set_type(ComplexSerializer())

        self.image_array = ArrayField()
        self.image_array.set_type(ByteArrayField())

        self.dict = DictionaryField()
        self.dict.set_types(LongField(), AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "GenerateMoleculeImage"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.image_array, value)

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        ligands = context.read_using_serializer(self.complex_array)
        x = context.read_int()
        y = context.read_int()
        return ligands, (x, y)


class ImportFileSerializer(TypeSerializer):

    def version(self):
        return 0

    def name(self):
        return "ImportFile"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return


class ImportSmilesSerializer(TypeSerializer):
    def __init__(self):
        self.complex_array = ArrayField()
        self.complex_array.set_type(ComplexSerializer())
        self.string_array = ArrayField()
        self.string_array.set_type(StringField())

        self.dict = DictionaryField()
        self.dict.set_types(LongField(), AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "ImportSmiles"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.complex_array, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        strings = context.read_using_serializer(self.string_array)
        return strings


class RemoveHydrogenSerializer(TypeSerializer):
    def __init__(self):
        self.array_serializer = ArrayField()
        self.array_serializer.set_type(ComplexSerializer())
        atom_serializer = AtomSerializer()
        long_serializer = LongField()
        self.dict = DictionaryField()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "RemoveHydrogen"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.array_serializer, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.array_serializer)
        return complexes


class StartMinimizationSerializer(TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "StartMinimization"

    def serialize(self, version, value, context):
        context.write_bool(value)

    def deserialize(self, version, context):
        forcefield = context.read_byte()
        steps = context.read_int()
        steepest = context.read_bool()
        cutoff = context.read_float()
        return (forcefield, steps, steepest, cutoff)


class StopMinimizationSerializer(TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "StopMinimization"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return None


class StructurePrepSerializer(TypeSerializer):
    def __init__(self):
        self.array_serializer = ArrayField()
        self.array_serializer.set_type(ComplexSerializer())
        atom_serializer = AtomSerializer()
        long_serializer = LongField()
        self.dict = DictionaryField()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "StructurePrep"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.array_serializer, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.array_serializer)
        return complexes


class IntegrationSerializer(TypeSerializer):
    __hash_serializer_map = {
        Hashes.IntegrationHashes[IntegrationCommands.hydrogen_add]: AddHydrogenSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.hydrogen_remove]: RemoveHydrogenSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.structure_prep]: StructurePrepSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.calculate_esp]: CalculateESPSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.minimization_start]: StartMinimizationSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.minimization_stop]: StopMinimizationSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.export_locations]: ExportLocationsSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.export_file]: ExportFileSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.import_file]: ImportFileSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.generate_molecule_image]: GenerateMoleculeImageSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.export_smiles]: ExportSmilesSerializer(),
        Hashes.IntegrationHashes[IntegrationCommands.import_smiles]: ImportSmilesSerializer()
    }

    def version(self):
        return 0

    def name(self):
        return "Integration"

    def serialize(self, version, value, context):
        context.write_uint(value[0])
        context.write_uint(value[1])
        val_to_write = value[2]
        serializer = self.__hash_serializer_map[value[1]]
        context.write_using_serializer(
            serializer, val_to_write)

    def deserialize(self, version, context):
        request_id = context.read_uint()
        hash = context.read_uint()
        arg = context.read_using_serializer(self.__hash_serializer_map[hash])
        return (request_id, hash, arg)
