from nanome._internal.serializer_fields import TypeSerializer, ArraySerializer, DictionarySerializer, LongSerializer, ByteArraySerializer, LongSerializer, StringSerializer
from nanome.api.structure.serializers import ComplexSerializer, AtomSerializer


class AddHydrogen(TypeSerializer):
    def __init__(self):
        self.array_serializer = ArraySerializer()
        self.array_serializer.set_type(ComplexSerializer())
        atom_serializer = AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
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
        self.array_serializer = ArraySerializer()
        self.array_serializer.set_type(ComplexSerializer())
        atom_serializer = AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
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
    _String = StringSerializer()

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
        self.array = ArraySerializer()
        self.array.set_type(StringSerializer())

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
        self.complex_array = ArraySerializer()
        self.complex_array.set_type(ComplexSerializer())
        self.string_array = ArraySerializer()
        self.string_array.set_type(StringSerializer())

        self.dict = DictionarySerializer()
        self.dict.set_types(LongSerializer(), AtomSerializer())

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
        self.complex_array = ArraySerializer()
        self.complex_array.set_type(ComplexSerializer())

        self.image_array = ArraySerializer()
        self.image_array.set_type(ByteArraySerializer())

        self.dict = DictionarySerializer()
        self.dict.set_types(LongSerializer(), AtomSerializer())

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
        self.complex_array = ArraySerializer()
        self.complex_array.set_type(ComplexSerializer())
        self.string_array = ArraySerializer()
        self.string_array.set_type(StringSerializer())

        self.dict = DictionarySerializer()
        self.dict.set_types(LongSerializer(), AtomSerializer())

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
        self.array_serializer = ArraySerializer()
        self.array_serializer.set_type(ComplexSerializer())
        atom_serializer = AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
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
        self.array_serializer = ArraySerializer()
        self.array_serializer.set_type(ComplexSerializer())
        atom_serializer = AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
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