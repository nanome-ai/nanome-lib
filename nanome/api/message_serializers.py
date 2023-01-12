import logging

from nanome._internal import serializer_fields as serializer_fields
from nanome._internal.enums import IntegrationCommands
from nanome.api import integration
from nanome.api._hashes import Hashes


logger = logging.getLogger(__name__)

class Integration(serializer_fields.TypeSerializer):
    __integrations = {
        Hashes.IntegrationHashes[IntegrationCommands.hydrogen_add]: integration.messages.AddHydrogen(),
        Hashes.IntegrationHashes[IntegrationCommands.hydrogen_remove]: integration.messages.RemoveHydrogen(),
        Hashes.IntegrationHashes[IntegrationCommands.structure_prep]: integration.messages.StructurePrep(),
        Hashes.IntegrationHashes[IntegrationCommands.calculate_esp]: integration.messages.CalculateESP(),
        Hashes.IntegrationHashes[IntegrationCommands.minimization_start]: integration.messages.StartMinimization(),
        Hashes.IntegrationHashes[IntegrationCommands.minimization_stop]: integration.messages.StopMinimization(),
        Hashes.IntegrationHashes[IntegrationCommands.export_locations]: integration.messages.ExportLocations(),
        Hashes.IntegrationHashes[IntegrationCommands.export_file]: integration.messages.ExportFile(),
        Hashes.IntegrationHashes[IntegrationCommands.import_file]: integration.messages.ImportFile(),
        Hashes.IntegrationHashes[IntegrationCommands.generate_molecule_image]: integration.messages.GenerateMoleculeImage(),
        Hashes.IntegrationHashes[IntegrationCommands.export_smiles]: integration.messages.ExportSmiles(),
        Hashes.IntegrationHashes[IntegrationCommands.import_smiles]: integration.messages.ImportSmiles(
        )
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
        context.write_using_serializer(
            Integration.__integrations[value[1]], value[2])

    def deserialize(self, version, context):
        requestID = context.read_uint()
        type = context.read_uint()
        arg = context.read_using_serializer(Integration.__integrations[type])
        return (requestID, type, arg)
