from nanome._internal.serializer_fields import TypeSerializer, ArrayField, DictionaryField, LongField, ByteArrayField, LongField, StringField
from nanome._internal.enums import IntegrationCommands
from nanome.api._hashes import Hashes
from nanome.api.structure.serializers import ComplexSerializer, AtomSerializer


class AddHydrogen(TypeSerializer):
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


class CalculateESP(TypeSerializer):
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


class ExportFile(TypeSerializer):
    _String = StringField()

    def version(self):
        return 0

    def name(self):
        return "ExportFile"

    def serialize(self, version, value, context):
        context.write_bool(value)

    def deserialize(self, version, context):
        location = context.read_using_serializer(ExportFile._String)
        filename = context.read_using_serializer(ExportFile._String)
        data = context.read_byte_array()
        return (location, filename, data)


class ExportLocations(TypeSerializer):
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


class ExportSmiles(TypeSerializer):
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


class GenerateMoleculeImage(TypeSerializer):
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


class ImportFile(TypeSerializer):

    def version(self):
        return 0

    def name(self):
        return "ImportFile"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return


class ImportSmiles(TypeSerializer):
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


class RemoveHydrogen(TypeSerializer):
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


class StartMinimization(TypeSerializer):
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


class StopMinimization(TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "StopMinimization"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return None


class StructurePrep(TypeSerializer):
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


class Integration(TypeSerializer):
    __integrations = {
        Hashes.IntegrationHashes[IntegrationCommands.hydrogen_add]: AddHydrogen(),
        Hashes.IntegrationHashes[IntegrationCommands.hydrogen_remove]: RemoveHydrogen(),
        Hashes.IntegrationHashes[IntegrationCommands.structure_prep]: StructurePrep(),
        Hashes.IntegrationHashes[IntegrationCommands.calculate_esp]: CalculateESP(),
        Hashes.IntegrationHashes[IntegrationCommands.minimization_start]: StartMinimization(),
        Hashes.IntegrationHashes[IntegrationCommands.minimization_stop]: StopMinimization(),
        Hashes.IntegrationHashes[IntegrationCommands.export_locations]: ExportLocations(),
        Hashes.IntegrationHashes[IntegrationCommands.export_file]: ExportFile(),
        Hashes.IntegrationHashes[IntegrationCommands.import_file]: ImportFile(),
        Hashes.IntegrationHashes[IntegrationCommands.generate_molecule_image]: GenerateMoleculeImage(),
        Hashes.IntegrationHashes[IntegrationCommands.export_smiles]: ExportSmiles(),
        Hashes.IntegrationHashes[IntegrationCommands.import_smiles]: ImportSmiles(
        )
    }

    def version(self):
        return 0

    def name(self):
        return "Integration"

    def serialize(self, version, value, context):
        context.write_uint(value[0])
        context.write_uint(value[1])
        context.write_using_serializer(
            Integration.__integrations[value[1]], value[2])

    def deserialize(self, version, context):
        requestID = context.read_uint()
        type = context.read_uint()
        arg = context.read_using_serializer(Integration.__integrations[type])
        return (requestID, type, arg)
