


from nanome._internal.integration import serialization as Serializers
from nanome._internal.macro.serialization import _MacroSerializer
from nanome._internal.network.commands.callbacks import Hashes, Integrations
from nanome._internal.shapes.serialization import _SphereSerializer, _ShapeSerializer, _LineSerializer, _LabelSerializer, _MeshSerializer
from nanome._internal.structure import _Atom, _Bond, _Residue, _Chain, _Molecule, _Complex, _Base
from nanome._internal.structure.serialization import _ComplexSerializer, _MoleculeSerializer, _ChainSerializer, _ResidueSerializer, _BondSerializer, _AtomSerializer, _AtomSerializerID, _SubstructureSerializer, _AtomSerializer, _MoleculeSerializer, _WorkspaceSerializer
from nanome._internal.ui._serialization import _LayoutNodeSerializer, _UIBaseSerializer, _MenuSerializer, _LayoutNodeSerializerDeep
from nanome._internal.util.type_serializers import (
    ArraySerializer, LongSerializer, TypeSerializer,
    DictionarySerializer, LongSerializer, TupleSerializer, IntSerializer,
    UnityPositionSerializer, UnityRotationSerializer, Vector3Serializer, StringSerializer,
    ColorSerializer, DirectoryEntrySerializer, FileDataSerializer, FileSaveDataSerializer, ByteSerializer)
from nanome._internal.volumetric.serialization import _VolumeDataSerializer, _VolumePropertiesSerializer
from nanome.util import DirectoryRequestResult, DirectoryErrorCode, FileError, IntEnum, Quaternion, Logs
from nanome.util.enums import LoadFileErrorCode, ShapeType,StreamDataType, StreamDirection,StreamType as SType
from nanome.util.file import FileMeta, LoadInfoDone
import types


class ApplyColorScheme(TypeSerializer):
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


class AdvancedSettings(TypeSerializer):
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


class Connect(TypeSerializer):
    def __init__(self):
        self.__dictionary = DictionarySerializer()
        self.__dictionary.set_types(StringSerializer(), ByteSerializer())

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


class Run(TypeSerializer):
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


class SetPluginListButton(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

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


class CD(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "cd"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class CP(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "cp"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value[0])
        context.write_using_serializer(self.__string, value[1])

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class ExportFilesItem(TypeSerializer):
    def __init__(self):
        self.__complex = _ComplexSerializer()
        self.__string = StringSerializer()
        self.__dict = DictionarySerializer()
        self.__dict.set_types(LongSerializer(), _AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "ExportFilesItem"

    def serialize(self, version, value, context):
        if isinstance(value, _Complex):
            context.write_byte(1)
            subcontext = context.create_sub_context()
            subcontext.payload["Atom"] = {}
            subcontext.write_using_serializer(self.__complex, value)
            context.write_using_serializer(
                self.__dict, subcontext.payload["Atom"])
            context.write_bytes(subcontext.to_array())
        elif isinstance(value, int):
            context.write_byte(0)
            context.write_long(value)
        else:
            raise TypeError(
                'Trying to serialize an unsupported type for export files')

    def deserialize(self, version, context):
        result_type = context.read_byte()
        if result_type == 0:
            return context.read_using_serializer(self.__string)
        elif result_type == 1:
            res = context.read_byte_array()
            if len(res) == 0:
                return None
            return res


class ExportFiles(TypeSerializer):
    def __init__(self):
        self.__array = ArraySerializer()
        self.__array.set_type(ExportFilesItem())

    def version(self):
        return 0

    def name(self):
        return "ExportFiles"

    def serialize(self, version, value, context):
        context.write_byte(int(value[0]))
        if (value[1] != None):
            context.write_bool(True)
            context.write_using_serializer(self.__array, value[1])
        else:
            context.write_bool(False)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__array)


class FileMeta(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "FileMeta"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value.name)
        context.write_long(value.size)
        context.write_using_serializer(self.__string, value.date_modified)
        context.write_bool(value.is_directory)

    def deserialize(self, version, context):
        result = FileMeta()
        result.name = context.read_using_serializer(self.__string)
        result.size = context.read_long()
        result.date_modified = context.read_using_serializer(self.__string)
        result.is_directory = context.read_bool()
        return result


class Get(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "get"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        error_code = FileError(context.read_int())
        length = context.read_uint()
        file = context.read_bytes(length)
        return (error_code, file)


class LS(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()
        self.__array = ArraySerializer()
        self.__array.set_type(FileMeta())

    def version(self):
        return 0

    def name(self):
        return "ls"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        error_code = FileError.safe_cast(context.read_int())
        filemetas = context.read_using_serializer(self.__array)
        return error_code, filemetas


class MKDir(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "mkdir"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class MV(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "mv"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value[0])
        context.write_using_serializer(self.__string, value[1])

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class Put(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "put"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value[0])
        context.write_uint(len(value[1]))
        context.write_bytes(value[1])

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class PWD(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "pwd"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        error_code = FileError.safe_cast(context.read_int())
        path = context.read_using_serializer(self.__string)
        return (error_code, path)


class RM(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "rm"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class RMDir(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "rmdir"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class DirectoryRequest(TypeSerializer):
    # Deprecated
    def __init__(self):
        self.__string = StringSerializer()
        self.__directory_entry_array = ArraySerializer()
        self.__directory_entry_array.set_type(DirectoryEntrySerializer())

    def version(self):
        return 0

    def name(self):
        return "Directory"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value._directory_name)
        context.write_using_serializer(self.__string, value._pattern)

    def deserialize(self, version, context):
        result = DirectoryRequestResult()
        result.entry_array = context.read_using_serializer(
            self.__directory_entry_array)
        result.error_code = DirectoryErrorCode(context.read_int())
        return result


class FileRequest(TypeSerializer):
    # Deprecated
    def __init__(self):
        self.__string_array = ArraySerializer()
        self.__string_array.set_type(StringSerializer())
        self.__file_data_array = ArraySerializer()
        self.__file_data_array.set_type(FileDataSerializer())

    def version(self):
        return 0

    def name(self):
        return "FileRequest"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string_array, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__file_data_array)


class FileSave(TypeSerializer):
    # Deprecated
    def __init__(self):
        self.__file_data_array = ArraySerializer()
        self.__file_data_array.set_type(FileSaveDataSerializer())

    def version(self):
        return 0

    def name(self):
        return "FileSave"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__file_data_array, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__file_data_array)


class Integration(TypeSerializer):
    __integrations = {
        Hashes.IntegrationHashes[Integrations.hydrogen_add]: Serializers._AddHydrogen(),
        Hashes.IntegrationHashes[Integrations.hydrogen_remove]: Serializers._RemoveHydrogen(),
        Hashes.IntegrationHashes[Integrations.structure_prep]: Serializers._StructurePrep(),
        Hashes.IntegrationHashes[Integrations.calculate_esp]: Serializers._CalculateESP(),
        Hashes.IntegrationHashes[Integrations.minimization_start]: Serializers._StartMinimization(),
        Hashes.IntegrationHashes[Integrations.minimization_stop]: Serializers._StopMinimization(),
        Hashes.IntegrationHashes[Integrations.export_locations]: Serializers._ExportLocations(),
        Hashes.IntegrationHashes[Integrations.export_file]: Serializers._ExportFile(),
        Hashes.IntegrationHashes[Integrations.import_file]: Serializers._ImportFile(),
        Hashes.IntegrationHashes[Integrations.generate_molecule_image]: Serializers._GenerateMoleculeImage(),
        Hashes.IntegrationHashes[Integrations.export_smiles]: Serializers._ExportSmiles(),
        Hashes.IntegrationHashes[Integrations.import_smiles]: Serializers._ImportSmiles(
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


class LoadFileInfo(TypeSerializer):
    def __init__(self):
        self.string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "LoadFileInfo"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value[0])
        context.write_byte_array(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError


class LoadFile(TypeSerializer):
    def __init__(self):
        self.array = ArraySerializer()
        self.array.set_type(LoadFileInfo())

    def version(self):
        return 0

    def name(self):
        return "LoadFile"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.array, value[0])
        context.write_bool(value[1])
        context.write_bool(value[2])

    def deserialize(self, version, context):
        raise NotImplementedError


class LoadFileDoneInfo(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "LoadFileDoneInfo"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        result = LoadInfoDone()
        result.success = LoadFileErrorCode(context.read_byte())
        return result


class LoadFileDone(TypeSerializer):
    def __init__(self):
        self.array = ArraySerializer()
        self.array.set_type(LoadFileDoneInfo())

    def version(self):
        return 0

    def name(self):
        return "LoadFileDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return context.read_using_serializer(self.array)

# classes


macro_serializer = _MacroSerializer()
string_serializer = StringSerializer()


class SaveMacro(TypeSerializer):
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


class DeleteMacro(TypeSerializer):
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


class RunMacro(TypeSerializer):
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


class GetMacros(TypeSerializer):
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


class GetMacrosResponse(TypeSerializer):
    _macro_serializer = macro_serializer
    _string_serializer = string_serializer

    def __init__(self):
        self._array_serializer = ArraySerializer()
        self._array_serializer.set_type(self._macro_serializer)

    def version(self):
        return 0

    def name(self):
        return "GetMacrosResponse"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return context.read_using_serializer(self._array_serializer)


class StopMacro(TypeSerializer):
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


class OpenURL(TypeSerializer):
    def __init__(self):
        self.string = StringSerializer()

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


class SendNotification(TypeSerializer):
    def __init__(self):
        self.string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "SendNotification"

    def serialize(self, version, value, context):
        context.write_uint(value[0])
        context.write_using_serializer(self.string, value[1])

    def deserialize(self, version, context):
        raise NotImplementedError


class SetSkybox(TypeSerializer):
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


class DeleteShape(TypeSerializer):
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
                Logs.warning(msg)
                raise TypeError(msg)
            context.write_int(value[0])
        elif version == 1:
            context.write_int_array(value)

    def deserialize(self, version, context):
        if version == 0:
            return [context.read_bool()]
        elif version == 1:
            return context.read_byte_array()


class SetShape(TypeSerializer):
    def __init__(self):
        self._position = UnityPositionSerializer()
        self._rotation = UnityRotationSerializer()
        self._color = ColorSerializer()
        self._sphere = _SphereSerializer()
        self._line = _LineSerializer()
        self._label = _LabelSerializer()
        self._mesh = _MeshSerializer()
        self._shape = _ShapeSerializer()
        self._shape_array = ArraySerializer()
        self._shape_array.set_type(self._shape)

    def version(self):
        return 2

    def name(self):
        return "SetShape"

    def serialize(self, version, value, context):
        if version == 0:
            if len(value) > 1:
                msg = "SetShape: Using a list of shapes with an old version of Nanome"
                Logs.warning(msg)
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
                Logs.warning(msg)
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


class CreateStream(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 2

    def name(self):
        return "StreamCreation"

    def serialize(self, version, value, context):
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


class CreateStreamResult(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 2

    def name(self):
        return "StreamCreationResult"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
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


class DestroyStream(TypeSerializer):
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


class FeedStream(TypeSerializer):
    def __init__(self):
        self.__array = ArraySerializer()
        self.__array.set_type(StringSerializer())

    def version(self):
        return 2

    def name(self):
        return "StreamFeed"

    def serialize(self, version, value, context):
        from nanome.api.streams import Stream

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
        from nanome.api.streams import Stream

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


class FeedStreamDone(TypeSerializer):
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


class InterruptStream(TypeSerializer):
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


class ButtonCallback(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 2

    def name(self):
        return "ButtonCallback"

    def serialize(self, version, value, context):
        id = value[0]
        state = value[1]
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            id |= plugin_mask
        context.write_int(id)
        if version >= 2:
            context.write_bool(state)

    def deserialize(self, version, context):
        content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            content_id &= id_mask
        state = False
        if version >= 2:
            state = context.read_bool()
        return (content_id, state)


class DropdownCallback(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "DropdownCallback"

    def serialize(self, version, value, context):
        # value is a tuple containing the image ID and the item index.
        context.write_int(value[0])
        context.write_int(value[1])

    def deserialize(self, version, context):
        id = context.read_int()
        item_index = context.read_int()
        return id, item_index


class GetMenuTransform(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "GetMenuTransform"

    def serialize(self, version, value, context):
        context.write_byte(value)

    def deserialize(self, version, context):
        return None


class GetMenuTransformResponse(TypeSerializer):
    def __init__(self):
        self.pos = UnityPositionSerializer()
        self.rot = UnityRotationSerializer()
        self.vec3 = Vector3Serializer()

    def version(self):
        return 0

    def name(self):
        return "GetMenuTransformResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        menu_position = context.read_using_serializer(self.pos)
        menu_rotation = context.read_using_serializer(self.rot)
        menu_scale = context.read_using_serializer(self.vec3)

        result = (menu_position, menu_rotation, menu_scale)
        return result


class ImageCallback(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "ImageCallback"

    def serialize(self, version, value, context):
        # value is a tuple containing the image ID, the x coordinate and the y coordinate.
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            value = (value[0] | plugin_mask, value[1], value[2])
        context.write_int(value[0])
        context.write_float(value[1])
        context.write_float(value[2])

    def deserialize(self, version, context):
        id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            id &= id_mask
        x = context.read_float()
        y = context.read_float()
        return id, x, y


class MenuCallback(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "MenuCallback"

    def serialize(self, version, value, context):
        if version >= 1:
            context.write_byte(value[0])
        context.write_bool(value[1])

    def deserialize(self, version, context):
        if version >= 1:
            index = context.read_byte()
        else:
            index = 0
        value = context.read_bool()
        return (index, value)


class SetMenuTransform(TypeSerializer):
    def __init__(self):
        self.pos = UnityPositionSerializer()
        self.rot = UnityRotationSerializer()
        self.vec3 = Vector3Serializer()

    def version(self):
        return 0

    def name(self):
        return "SetMenuTransform"

    def serialize(self, version, value, data):
        data.write_byte(value[0])
        data.write_using_serializer(self.pos, value[1])
        data.write_using_serializer(self.rot, value[2])
        data.write_using_serializer(self.vec3, value[3])

    def deserialize(self, version, data):
        return None


class SliderCallback(TypeSerializer):
    def version(self):
        return 1

    def name(self):
        return "SliderCallback"

    def serialize(self, version, value, context):
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            value[0] |= plugin_mask
        context.write_int(value[0])
        context.write_float(value[1])

    def deserialize(self, version, context):
        content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            content_id &= id_mask
        result = (content_id, context.read_float())
        return result


class TextInputCallback(TypeSerializer):
    def __init__(self):
        self.__tuple = TupleSerializer(IntSerializer(), StringSerializer())

    def version(self):
        return 1

    def name(self):
        return "TextInputCallback"

    def serialize(self, version, value, context):
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            value[0] |= plugin_mask
        context.write_using_serializer(self.__tuple, value)

    def deserialize(self, version, context):
        tup = context.read_using_serializer(self.__tuple)
        if (version == 0):
            id_mask = 0x00FFFFFF
            tup = (tup[0] & id_mask, tup[1])
        return tup


class UIHook(TypeSerializer):
    class Type(IntEnum):
        button_hover = 0
        image_pressed = 1
        image_held = 2
        image_released = 3

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "UIHook"

    def serialize(self, version, value, context):
        context.write_byte(value[0])
        context.write_int(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError


class UpdateContent(TypeSerializer):
    def __init__(self):
        self._array = ArraySerializer()
        self._content = _UIBaseSerializer()
        self._array.set_type(self._content)

    def version(self):
        return 1

    def name(self):
        return "SendUIContent"

    def serialize(self, version, value, context):
        if version == 0:
            context.write_using_serializer(self._content, value[0])
        else:
            context.write_using_serializer(self._array, value)

    def deserialize(self, version, context):
        return None


class UpdateMenu(TypeSerializer):
    def __init__(self):
        self.menu = _MenuSerializer()
        self.array = ArraySerializer()
        self.layout = _LayoutNodeSerializer()
        self.content = _UIBaseSerializer()

    def version(self):
        return 2

    def name(self):
        return "UpdateMenu"

    def serialize(self, version, value, context):
        (menu, shallow) = value
        if version >= 1:
            context.write_byte(menu.index)
        if version >= 2:
            context.write_bool(shallow)

        context.write_using_serializer(self.menu, menu)
        nodes = []
        content = []
        if not shallow:
            nodes = menu._get_all_nodes()
            content = menu._get_all_content()
        self.array.set_type(self.layout)
        context.write_using_serializer(self.array, nodes)
        self.array.set_type(self.content)
        context.write_using_serializer(self.array, content)

    def deserialize(self, version, context):
        return None


class UpdateNode(TypeSerializer):
    def __init__(self):
        self._array = ArraySerializer()
        self._node_serializer = _LayoutNodeSerializerDeep()
        self._array.set_type(self._node_serializer)

    def version(self):
        return 1

    def name(self):
        return "SendLayoutNode"

    def serialize(self, version, value, context):
        if version == 0:
            context.write_using_serializer(self._node_serializer, value[0])
        else:
            context.write_using_serializer(self._array, value)

    def deserialize(self, version, context):
        return None


class GetControllerTransforms(TypeSerializer):
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


class GetControllerTransformsResponse(TypeSerializer):
    def __init__(self):
        self.pos = UnityPositionSerializer()
        self.rot = UnityRotationSerializer()

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


class GetPresenterInfo(TypeSerializer):
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


class GetPresenterInfoResponse(TypeSerializer):
    def __init__(self):
        self.string = StringSerializer()

    def version(self):
        return 1

    def name(self):
        return "GetPresenterInfoResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        from nanome.api.user import PresenterInfo

        result = PresenterInfo()
        result.account_id = context.read_using_serializer(self.string)
        result.account_name = context.read_using_serializer(self.string)
        result.account_email = context.read_using_serializer(self.string)
        result.has_org = context.read_bool()
        if result.has_org:
            result.org_id = context.read_int()
            result.org_name = context.read_using_serializer(self.string)

        return result


class PresenterChange(TypeSerializer):
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


class AddVolume(TypeSerializer):
    def __init__(self):
        self.__complex = _ComplexSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = LongSerializer()
        self.__dict = DictionarySerializer()
        self.__dict.set_types(long_serializer, atom_serializer)
        self.__data = _VolumeDataSerializer()
        self.__properties = _VolumePropertiesSerializer()

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


class AddVolumeDone(TypeSerializer):
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


class AddBonds(TypeSerializer):
    def __init__(self):
        self.__array = ArraySerializer()
        self.__array.set_type(_ComplexSerializer())
        self.__dict = DictionarySerializer()
        self.__dict.set_types(LongSerializer(), _AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "AddBonds"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}

        subcontext.write_using_serializer(self.__array, value)

        context.write_using_serializer(self.__dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.__dict)
        complexes = context.read_using_serializer(self.__array)
        return complexes


class AddDSSP(TypeSerializer):
    def __init__(self):
        self.__array = ArraySerializer()
        self.__array.set_type(_ComplexSerializer())
        self.__dict = DictionarySerializer()
        self.__dict.set_types(LongSerializer(), _AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "AddDSSP"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}

        subcontext.write_using_serializer(self.__array, value)

        context.write_using_serializer(self.__dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.__dict)
        complexes = context.read_using_serializer(self.__array)
        return complexes


class AddToWorkspace(TypeSerializer):
    def __init__(self):
        self.__array = ArraySerializer()
        self.__array.set_type(_ComplexSerializer())
        atom_serializer = _AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "AddToWorkspace"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.__array, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.__array)
        return complexes


class ComplexAddedRemoved(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "ComplexAddedRemoved"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class ComplexUpdated(TypeSerializer):
    def __init__(self):
        self.complex_serializer = _ComplexSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "ComplexUpdated"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        index = context.read_long()
        has_complex = context.read_bool()

        if has_complex:
            context.payload["Atom"] = context.read_using_serializer(self.dict)
            complex = context.read_using_serializer(self.complex_serializer)
        else:
            complex = None
        return (index, complex)


class ComplexUpdatedHook(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "ComplexUpdatedHook"

    def serialize(self, version, value, context):
        context.write_long(value)

    def deserialize(self, version, context):
        raise NotImplementedError


class ComputeHBonds(TypeSerializer):
    def __init__(self):
        pass

    def name(self):
        return "ComputeHBonds"

    def version(self):
        return 0

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return None


# from nanome._internal.structure.serialization import _Long

# deep


class PositionStructures(TypeSerializer):
    def __init__(self):
        pass

    def name(self):
        return "PositionStructures"

    def version(self):
        return 0

    def serialize(self, version, value, context):
        # value is a structure[]
        if not isinstance(value, list) and not isinstance(value, types.GeneratorType):
            value = [value]

        atom_ids = []

        for val in value:
            if isinstance(val, _Atom):
                atom_ids.append(val._index)
            elif isinstance(val, _Bond):
                atom_ids.append(val._atom1._index)
                atom_ids.append(val._atom2._index)
            # all other base objects implement the atoms generator
            elif isinstance(val, _Base):
                for atom in val.atoms:
                    atom_ids.append(atom._index)

        context.write_long_array(atom_ids)

    def deserialize(self, version, context):
        return None


class PositionStructuresDone(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "PositionStructuresDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None


# shallow


class ReceiveComplexList(TypeSerializer):
    def __init__(self):
        self.array_serializer = ArraySerializer()
        self.array_serializer.set_type(_ComplexSerializer())

    def version(self):
        return 0

    def name(self):
        return "ReceiveComplexList"

    def serialize(self, version, value, context):
        raise NotImplementedError
        #context.write_using_serializer(self.array_serializer, value)

    def deserialize(self, version, data):
        complexes = data.read_using_serializer(self.array_serializer)

        return complexes

# deep


class ReceiveComplexes(TypeSerializer):
    def __init__(self):
        self.array_serializer = ArraySerializer()
        self.array_serializer.set_type(_ComplexSerializer())
        atom_serializer = _AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "ReceiveComplexes"

    def serialize(self, version, value, context):
        raise NotImplementedError
        #context.write_using_serializer(self.array_serializer, value)

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.array_serializer)
        return complexes


class ReceiveWorkspace(TypeSerializer):
    def __init__(self):
        self.workspace = _WorkspaceSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "ReceiveWorkspace"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        workspace = context.read_using_serializer(self.workspace)
        return workspace


class RequestComplexList(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "RequestComplexList"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return None


class RequestComplexes(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "RequestComplexes"

    def serialize(self, version, value, context):
        context.write_long_array(value)

    def deserialize(self, version, context):
        return None


class RequestSubstructure(TypeSerializer):
    def __init__(self):
        self.array = ArraySerializer()
        self.array.set_type(_SubstructureSerializer())
        self.dict = DictionarySerializer()
        self.dict.set_types(LongSerializer(), _AtomSerializer())
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
            substructure._residues = [residue_map[index]
                                      for index in substructure._residues]
        return substructures


class RequestWorkspace(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "RequestWorkspace"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class SelectionChanged(TypeSerializer):
    def __init__(self):
        self.complex_serializer = _ComplexSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "SelectionChanged"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        index = context.read_long()
        has_complex = context.read_bool()

        if has_complex:
            context.payload["Atom"] = context.read_using_serializer(self.dict)
            complex = context.read_using_serializer(self.complex_serializer)
        else:
            complex = None
        return (index, complex)


class SelectionChangedHook(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "SelectionChangedHook"

    def serialize(self, version, value, context):
        context.write_long(value)

    def deserialize(self, version, context):
        raise NotImplementedError


# deep


class UpdateStructures(TypeSerializer):
    def __init__(self, shallow):
        self.array_serializer = ArraySerializer()
        # setting the shallow flag
        self.complex_serializer = _ComplexSerializer(shallow)
        self.molecule_serializer = _MoleculeSerializer(shallow)
        self.chain_serializer = _ChainSerializer(shallow)
        self.residue_serializer = _ResidueSerializer(shallow)
        self.bond_serializer = _BondSerializer(shallow)
        self.atom_serializer = _AtomSerializerID(shallow)
        # atom dict only used by deep
        self.dict = DictionarySerializer()
        self.dict.set_types(LongSerializer(), _AtomSerializer())

    def name(self):
        return "UpdateStructures"

    def version(self):
        return 0

    def serialize(self, version, value, context):
        # value is a structure[]

        atoms = []
        bonds = []
        residues = []
        chains = []
        molecules = []
        complexes = []

        for val in value:
            if isinstance(val, _Atom):
                atoms.append(val)
            if isinstance(val, _Bond):
                bonds.append(val)
            if isinstance(val, _Residue):
                residues.append(val)
            if isinstance(val, _Chain):
                chains.append(val)
            if isinstance(val, _Molecule):
                molecules.append(val)
            if isinstance(val, _Complex):
                complexes.append(val)

        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}

        self.array_serializer.set_type(self.complex_serializer)
        subcontext.write_using_serializer(self.array_serializer, complexes)
        self.array_serializer.set_type(self.molecule_serializer)
        subcontext.write_using_serializer(self.array_serializer, molecules)
        self.array_serializer.set_type(self.chain_serializer)
        subcontext.write_using_serializer(self.array_serializer, chains)
        self.array_serializer.set_type(self.residue_serializer)
        subcontext.write_using_serializer(self.array_serializer, residues)
        self.array_serializer.set_type(self.bond_serializer)
        subcontext.write_using_serializer(self.array_serializer, bonds)
        self.array_serializer.set_type(self.atom_serializer)
        subcontext.write_using_serializer(self.array_serializer, atoms)

        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

        for complex in complexes:
            complex._surface_dirty = False

    def deserialize(self, version, context):
        return None


class UpdateStructuresDeepDone(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "UpdateStructureDeepDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None


class UpdateWorkspace(TypeSerializer):
    def __init__(self):
        self.workspace = _WorkspaceSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "UpdateWorkspace"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.workspace, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        raise NotImplementedError
