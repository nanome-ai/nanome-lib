from nanome._internal._util._serializers import _StringSerializer, _ColorSerializer, _Vector3Serializer
from .. import _Atom

# Requires a dictionary of Atoms.
# Serializes the atoms serial instead of the whole atom but adds it to the dict
# Deserializes the ID and returns the atom from the dict with that ID.
from nanome._internal._util._serializers import _TypeSerializer

class _AtomSerializerID(_TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "AtomIndex"

    def serialize(self, version, value, context):
        context.write_long(value._unique_identifier)
        payload = context.payload["Atom"]
        payload[value._unique_identifier] = value

    def deserialize(self, version, context):
        uid = context.read_long()
        payload = context.payload["Atom"]
        atom = payload[uid]
        return atom