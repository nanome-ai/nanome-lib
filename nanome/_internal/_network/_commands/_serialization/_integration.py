from nanome._internal._util._serializers import _TypeSerializer
from nanome._internal._network._commands._callbacks._commands_enums import _Hashes
from nanome._internal._integration import _serialization as Serializers
from nanome.util.enums import Integrations

class _Integration(_TypeSerializer):
    __integrations = {
        _Hashes.IntegrationHashes[Integrations.hydrogen_add]: Serializers._AddHydrogen(),
        _Hashes.IntegrationHashes[Integrations.hydrogen_remove]: Serializers._RemoveHydrogen(),
        _Hashes.IntegrationHashes[Integrations.structure_prep]: Serializers._StructurePrep(),
        _Hashes.IntegrationHashes[Integrations.calculate_esp]: Serializers._CalculateESP(),
        _Hashes.IntegrationHashes[Integrations.minimization_start]: Serializers._StartMinimization(),
        _Hashes.IntegrationHashes[Integrations.minimization_stop]: Serializers._StopMinimization(),
        _Hashes.IntegrationHashes[Integrations.file_export]: Serializers._FileExport(),
        _Hashes.IntegrationHashes[Integrations.generate_molecule_image]: Serializers._GenerateMoleculeImage(),
    }

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "Integration"

    def serialize(self, version, value, context):
        context.write_uint(value[0])
        context.write_uint(value[1])
        context.write_using_serializer(_Integration.__integrations[value[1]], value[2])

    def deserialize(self, version, context):
        requestID = context.read_uint()
        type = context.read_uint()
        arg = context.read_using_serializer(_Integration.__integrations[type])
        return (requestID, type, arg)
