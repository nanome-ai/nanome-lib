from nanome._internal._util._serializers import _TypeSerializer, _ArraySerializer, _DictionarySerializer, _LongSerializer
from nanome._internal._structure._serialization import _SubstructureSerializer, _AtomSerializer, _MoleculeSerializer


class _RequestSubstructure(_TypeSerializer):
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
            substructure._residues = [residue_map[index] for index in substructure._residues]
        return substructures
