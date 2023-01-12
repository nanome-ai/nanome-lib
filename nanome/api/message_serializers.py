import logging
import types

from nanome._internal import serializer_fields as serializer_fields

from nanome._internal.enums import IntegrationCommands
from nanome._internal.enum_utils import IntEnum
from nanome.api import integration, structure, macro, shapes, ui, volumetric
from nanome.api._hashes import Hashes
from nanome.api.streams import Stream
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
        Hashes.IntegrationHashes[IntegrationCommands.hydrogen_add]: integration.serializers.AddHydrogen(),
        Hashes.IntegrationHashes[IntegrationCommands.hydrogen_remove]: integration.serializers.RemoveHydrogen(),
        Hashes.IntegrationHashes[IntegrationCommands.structure_prep]: integration.serializers.StructurePrep(),
        Hashes.IntegrationHashes[IntegrationCommands.calculate_esp]: integration.serializers.CalculateESP(),
        Hashes.IntegrationHashes[IntegrationCommands.minimization_start]: integration.serializers.StartMinimization(),
        Hashes.IntegrationHashes[IntegrationCommands.minimization_stop]: integration.serializers.StopMinimization(),
        Hashes.IntegrationHashes[IntegrationCommands.export_locations]: integration.serializers.ExportLocations(),
        Hashes.IntegrationHashes[IntegrationCommands.export_file]: integration.serializers.ExportFile(),
        Hashes.IntegrationHashes[IntegrationCommands.import_file]: integration.serializers.ImportFile(),
        Hashes.IntegrationHashes[IntegrationCommands.generate_molecule_image]: integration.serializers.GenerateMoleculeImage(),
        Hashes.IntegrationHashes[IntegrationCommands.export_smiles]: integration.serializers.ExportSmiles(),
        Hashes.IntegrationHashes[IntegrationCommands.import_smiles]: integration.serializers.ImportSmiles(
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


macro_serializer = macro.serializers.MacroSerializer()
string_serializer = serializer_fields.StringSerializer()


class SaveMacro(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "SaveMacro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._macro_serializer, value[0])
        context.write_bool(value[1])
        context.write_using_serializer(self._string_serializer, value[2])

    def deserialize(self, version, context):
        raise NotImplementedError


class DeleteMacro(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "DeleteMacro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._macro_serializer, value[0])
        context.write_bool(value[1])
        context.write_using_serializer(self._string_serializer, value[2])

    def deserialize(self, version, context):
        raise NotImplementedError


class RunMacro(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "RunMacro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._macro_serializer, value)

    def deserialize(self, version, context):
        if version < 1:
            return
        return context.read_bool()


class GetMacros(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "GetMacros"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._string_serializer, value)

    def deserialize(self, version, context):
        raise NotImplementedError


class GetMacrosResponse(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        self._array_serializer = serializer_fields.ArraySerializer()
        self._array_serializer.set_type(self._macro_serializer)

    def version(self):
        return 0

    def name(self):
        return "GetMacrosResponse"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return context.read_using_serializer(self._array_serializer)


class StopMacro(serializer_fields.TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "StopMacro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._string_serializer, value)

    def deserialize(self, version, context):
        raise NotImplementedError


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


class DeleteShape(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "DeleteShape"

    def serialize(self, version, value, context):
        if version == 0:
            if len(value) > 1:
                msg = "SetShape: Using a list of shapes with an old version of Nanome"
                logger.warning(msg)
                raise TypeError(msg)
            context.write_int(value[0])
        elif version == 1:
            context.write_int_array(value)

    def deserialize(self, version, context):
        if version == 0:
            return [context.read_bool()]
        elif version == 1:
            return context.read_byte_array()


class SetShape(serializer_fields.TypeSerializer):

    def __init__(self):
        self._position = serializer_fields.UnityPositionSerializer()
        self._rotation = serializer_fields.UnityRotationSerializer()
        self._color = serializer_fields.ColorSerializer()
        self._sphere = shapes.serializers.SphereSerializer()
        self._line = shapes.serializers.LineSerializer()
        self._label = shapes.serializers.LabelSerializer()
        self._mesh = shapes.serializers.MeshSerializer()
        self._shape = shapes.serializers.ShapeSerializer()
        self._shape_array = serializer_fields.ArraySerializer()
        self._shape_array.set_type(self._shape)

    def version(self):
        return 2

    def name(self):
        return "SetShape"

    def serialize(self, version, value, context):
        from nanome.util import Quaternion
        from nanome.util.enums import ShapeType
        if version == 0:
            if len(value) > 1:
                msg = "SetShape: Using a list of shapes with an old version of Nanome"
                logger.warning(msg)
                raise TypeError(msg)
            first_elem = value[0]
            context.write_byte(int(first_elem.shape_type))
            if first_elem.shape_type == ShapeType.Sphere:
                context.write_using_serializer(self._sphere, first_elem)
            if first_elem.shape_type == ShapeType.Line:
                context.write_using_serializer(self._line, first_elem)
            if first_elem.shape_type == ShapeType.Label:
                context.write_using_serializer(self._label, first_elem)
            if first_elem.shape_type == ShapeType.Mesh:
                context.write_using_serializer(self._mesh, first_elem)
            context.write_int(first_elem.index)
            context.write_long(first_elem.target)
            context.write_byte(int(first_elem.anchor))
            context.write_using_serializer(self._position, first_elem.position)
            context.write_using_serializer(self._rotation, Quaternion())
            context.write_using_serializer(self._color, first_elem.color)
        elif version == 1:
            if len(value) > 1:
                msg = "SetShape: Using a list of shapes with an old version of Nanome"
                logger.warning(msg)
                raise TypeError(msg)
            first_elem = value[0]
            context.write_using_serializer(self._shape, first_elem)
        elif version == 2:
            context.write_using_serializer(self._shape_array, value)

    def deserialize(self, version, context):
        if version < 2:
            return ([context.read_int()], [context.read_bool()])
        else:
            indices_arr = context.read_int_array()
            success_arr = context.read_byte_array()
            return (indices_arr, success_arr)


class CreateStream(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 2

    def name(self):
        return "StreamCreation"

    def serialize(self, version, value, context):
        from nanome.util.enums import StreamType as SType
        stream_type = value[0]
        if version > 0:
            context.write_byte(stream_type)
        if version >= 2:
            context.write_byte(value[2])

        if stream_type == SType.shape_position or stream_type == SType.shape_color or stream_type == SType.sphere_shape_radius:
            context.write_int_array(value[1])
        else:
            context.write_long_array(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError


class CreateStreamResult(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 2

    def name(self):
        return "StreamCreationResult"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        from nanome.util.enums import StreamDataType, StreamDirection
        err = context.read_byte()
        id = context.read_uint()
        if version > 0:
            data_type = StreamDataType(context.read_byte())
        else:
            data_type = StreamDataType.float
        if version >= 2:
            direction = StreamDirection(context.read_byte())
        else:
            direction = StreamDirection.writing
        return (err, id, data_type, direction)


class DestroyStream(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "StreamDestruction"

    def serialize(self, version, value, context):
        context.write_uint(value)

    def deserialize(self, version, context):
        raise NotImplementedError


class FeedStream(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__array = serializer_fields.ArraySerializer()
        self.__array.set_type(serializer_fields.StringSerializer())

    def version(self):
        return 2

    def name(self):
        return "StreamFeed"

    def serialize(self, version, value, context):

        context.write_uint(value[0])
        data_type = value[2]
        if version > 0:
            context.write_byte(data_type)
        if data_type == Stream.DataType.byte:
            context.write_byte_array(value[1])
        elif data_type == Stream.DataType.string:
            context.write_using_serializer(self.__array, value[1])
        else:
            context.write_float_array(value[1])

    def deserialize(self, version, context):

        id = context.read_uint()
        type = Stream.DataType.float
        if version > 0:
            type = Stream.DataType(context.read_byte())

        if type == Stream.DataType.byte:
            data = context.read_byte_array()
        elif type == Stream.DataType.string:
            data = context.read_using_serializer(self.__array)
        else:
            data = context.read_float_array()

        return (id, data, type)


class FeedStreamDone(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "StreamFeedDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None


class InterruptStream(serializer_fields.TypeSerializer):

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "StreamInterrupt"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        err = context.read_byte()
        id = context.read_uint()
        return (err, id)


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

