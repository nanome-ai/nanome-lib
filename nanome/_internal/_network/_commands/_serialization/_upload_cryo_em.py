from nanome._internal._network._serialization import _ContextDeserialization, _ContextSerialization
from nanome._internal._volumetric._serialization import _VolumeDataSerializer
from nanome._internal._util._serializers import _TypeSerializer
from nanome._internal._volumetric._io._em_map._parse import parse_file
class _UploadCryoEM(_TypeSerializer):
    def __init__(self):
        self.vd_serializer = _VolumeDataSerializer()

    def version(self):
        return 0

    def name(self):
        return "UploadCryoEM"

    def serialize(self, version, value, context):
        volume_data = parse_file(value)
        context.write_using_serializer(self.vd_serializer, volume_data)

    def deserialize(self, version, context):
        raise NotImplementedError