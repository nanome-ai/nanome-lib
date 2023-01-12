import logging

from nanome._internal import serializer_fields as serializer_fields
from nanome._internal.enums import IntegrationCommands
from nanome.api import integration, structure, volumetric
from nanome.api._hashes import Hashes
from nanome.api.user import PresenterInfo


logger = logging.getLogger(__name__)


class ApplyColorScheme(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "ApplyColorScheme"

    def serialize(self, version, value, context):
        context.write_int(value[0])
        context.write_int(value[1])
        context.write_bool(value[2])

    def deserialize(self, version, context):
        raise NotImplementedError


class AdvancedSettings(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "AdvancedSettings"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class Connect(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__dictionary = serializer_fields.DictionarySerializer()
        self.__dictionary.set_types(serializer_fields.StringSerializer(), serializer_fields.ByteSerializer())

    def version(self):
        return 0

    def name(self):
        return "Connect"

    def serialize(self, version, value, data):
        data.write_byte(value[0])
        data.write_using_serializer(self.__dictionary, value[1])

    def deserialize(self, version, data):
        version_table = data.read_using_serializer(self.__dictionary)
        return version_table


class Run(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "Run"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class SetPluginListButton(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "SetPluginListButton"

    def serialize(self, version, value, data):
        data.write_uint(value[0])
        data.write_using_serializer(self.__string, value[1])
        data.write_bool(value[2])

    def deserialize(self, version, data):
        return None


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


class OpenURL(serializer_fields.TypeSerializer):

    def __init__(self):
        self.string = serializer_fields.StringSerializer()

    def version(self):
        return 1

    def name(self):
        return "OpenURL"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value[0])  # URL
        if version >= 1:
            context.write_bool(value[1])  # Desktop Browser

    def deserialize(self, version, context):
        raise NotImplementedError


class SetSkybox(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "SetSkybox"

    def serialize(self, version, value, context):
        context.write_int(value)

    def deserialize(self, version, context):
        raise NotImplementedError



class GetControllerTransforms(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "GetControllerTransforms"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class GetControllerTransformsResponse(serializer_fields.TypeSerializer):

    def __init__(self):
        self.pos = serializer_fields.UnityPositionSerializer()
        self.rot = serializer_fields.UnityRotationSerializer()

    def version(self):
        return 0

    def name(self):
        return "GetControllerTransformsResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        headset_position = context.read_using_serializer(self.pos)
        headset_rotation = context.read_using_serializer(self.rot)
        left_controller_position = context.read_using_serializer(self.pos)
        left_controller_rotation = context.read_using_serializer(self.rot)
        right_controller_position = context.read_using_serializer(self.pos)
        right_controller_rotation = context.read_using_serializer(self.rot)

        result = (headset_position, headset_rotation, left_controller_position,
                  left_controller_rotation, right_controller_position, right_controller_rotation)
        return result


class GetPresenterInfo(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "GetPresenterInfo"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class GetPresenterInfoResponse(serializer_fields.TypeSerializer):

    def __init__(self):
        self.string = serializer_fields.StringSerializer()

    def version(self):
        return 1

    def name(self):
        return "GetPresenterInfoResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):

        result = PresenterInfo()
        result.account_id = context.read_using_serializer(self.string)
        result.account_name = context.read_using_serializer(self.string)
        result.account_email = context.read_using_serializer(self.string)
        result.has_org = context.read_bool()
        if result.has_org:
            result.org_id = context.read_int()
            result.org_name = context.read_using_serializer(self.string)

        return result


class PresenterChange(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "PresenterChange"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class AddVolume(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__complex = structure.serializers.ComplexSerializer()
        atom_serializer = structure.serializers.AtomSerializer()
        long_serializer = serializer_fields.LongSerializer()
        self.__dict = serializer_fields.DictionarySerializer()
        self.__dict.set_types(long_serializer, atom_serializer)
        self.__data = volumetric.serializers.VolumeDataSerializer()
        self.__properties = volumetric.serializers.VolumePropertiesSerializer()

    def version(self):
        return 0

    def name(self):
        return "AddVolume"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.__complex, value[0])
        context.write_using_serializer(self.__dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

        context.write_long(value[1])
        context.write_using_serializer(self.__data, value[2])
        context.write_using_serializer(self.__properties, value[3])

    def deserialize(self, version, context):
        raise NotImplementedError


class AddVolumeDone(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "AddVolumeDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None

