from nanome._internal.util.serializers import TypeSerializer
from nanome._internal.network.commands.callbacks.commands_enums import _Hashes, Integrations
from nanome._internal.integration import serialization as Serializers


class _Integration(TypeSerializer):
    __integrations = {
        _Hashes.IntegrationHashes[Integrations.hydrogen_add]: Serializers._AddHydrogen(),
        _Hashes.IntegrationHashes[Integrations.hydrogen_remove]: Serializers._RemoveHydrogen(),
        _Hashes.IntegrationHashes[Integrations.structure_prep]: Serializers._StructurePrep(),
        _Hashes.IntegrationHashes[Integrations.calculate_esp]: Serializers._CalculateESP(),
        _Hashes.IntegrationHashes[Integrations.minimization_start]: Serializers._StartMinimization(),
        _Hashes.IntegrationHashes[Integrations.minimization_stop]: Serializers._StopMinimization(),
        _Hashes.IntegrationHashes[Integrations.export_locations]: Serializers._ExportLocations(),
        _Hashes.IntegrationHashes[Integrations.export_file]: Serializers._ExportFile(),
        _Hashes.IntegrationHashes[Integrations.import_file]: Serializers._ImportFile(),
        _Hashes.IntegrationHashes[Integrations.generate_molecule_image]: Serializers._GenerateMoleculeImage(),
        _Hashes.IntegrationHashes[Integrations.export_smiles]: Serializers._ExportSmiles(),
        _Hashes.IntegrationHashes[Integrations.import_smiles]: Serializers._ImportSmiles()
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
