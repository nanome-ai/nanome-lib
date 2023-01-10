import sys
from abc import ABCMeta, abstractmethod

if sys.version_info >= (3, 0):
    def to_bytes(value, encoding):
        return bytes(value, 'utf-8')

else:
    def to_bytes(value, encoding):
        return bytearray(value, 'utf-8')

class TypeSerializer(object):

    __metaclass__ = ABCMeta
    __version_table = dict()

    def __new__(cls, *args):
        result = super(TypeSerializer, cls).__new__(cls)
        cls.register_string_raw(result.name(), result.version())
        result.__init__(*args)
        return result

    @classmethod
    def register_string_raw(cls, string, version):
        cls.__version_table[string] = version

    @classmethod
    def get_version_table(cls):
        return cls.__version_table

    @classmethod
    def get_best_version_table(cls, nanome_table):
        result = dict()
        version_table = cls.__version_table
        for key in nanome_table:
            nanome_version = nanome_table[key]
            try:
                version = version_table[key]
                result[key] = min(version, nanome_version)
            except:
                # logger.warning("Plugin Library might be outdated: received a serializer version for an unknown serializer:", key, "Version:", nanome_version)
                pass
        return result

    @abstractmethod
    def name(self):
        # type() -> str
        pass

    @abstractmethod
    def version(self):
        # type() -> int
        pass


class ArraySerializer(TypeSerializer):
    def __init__(self):
        self._serializer = None

    def version(self):
        return 0

    def name(self):
        return "Array"

    def serialize(self, version, value, context):
        if self._serializer == None:
            raise TypeError(
                'Trying to serialize array without setting content type first')

        context.write_uint(len(value))
        for cur in value:
            context.write_using_serializer(self._serializer, cur)

    def deserialize(self, version, context):
        if self._serializer == None:
            raise TypeError(
                'Trying to deserialize array without setting content type first')

        length = context.read_uint()
        result = []
        for _ in range(length):
            deserialized = context.read_using_serializer(self._serializer)
            result.append(deserialized)
        return result

    def set_type(self, serializer):
        self._serializer = serializer


class BoolSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "bool"

    def serialize(self, version, value, context):
        context.write_bool(value)

    def deserialize(self, version, context):
        return context.read_bool()


class ByteArraySerializer(TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "ByteArray"

    def serialize(self, version, value, context):
        context.write_byte_array(value)

    def deserialize(self, version, context):
        return context.read_byte_Array()


class ByteSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "byte"

    def serialize(self, version, value, context):
        context.write_byte(value)

    def deserialize(self, version, context):
        byte = context.read_byte()
        return byte


class CachedImageSerializer(TypeSerializer):
    cache = set()
    session = 0

    def __init__(self):
        self._string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "CachedImage"

    def serialize(self, version, value, context):
        session = CachedImageSerializer.session
        if value == None or value == "":
            context.write_bool(False)
            context.write_using_serializer(self._string, str(session) + "-")
            context.write_byte_array([])
            return

        if value in CachedImageSerializer.cache:
            context.write_bool(True)
            context.write_using_serializer(
                self._string, str(session) + "-" + value)
        else:
            with open(value, "rb") as f:
                data = f.read()
            context.write_bool(False)
            context.write_using_serializer(
                self._string, str(session) + "-" + value)
            context.write_byte_array(data)
            CachedImageSerializer.cache.add(value)

    def deserialize(self, version, context):
        # This function is only used by unit tests
        is_cached = context.read_bool()
        if is_cached:
            context.read_using_serializer(self._string)
        else:
            context.read_using_serializer(self._string)
            context.read_byte_array()


class CharSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "char"

    def serialize(self, version, value, context):
        context.write_byte(ord(value[0]))

    def deserialize(self, version, context):
        return chr(context.read_byte())


class ColorSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "Color"

    def serialize(self, version, value, context):
        context.write_uint(value._color)

    def deserialize(self, version, context):
        from nanome.util import Color
        return Color.from_int(context.read_uint())


class DictionarySerializer(TypeSerializer):
    def __init__(self):
        self._serializer = None

    def version(self):
        return 0

    def name(self):
        return "Dictionary"

    def serialize(self, version, value, context):
        if self._serializer == None:
            raise TypeError(
                'Trying to serialize dictionary without setting content type first')
        context.write_using_serializer(self._serializer, value.items())

    def deserialize(self, version, context):
        if self._serializer == None:
            raise TypeError(
                'Trying to deserialize dictionary without setting content type first')
        result = dict(context.read_using_serializer(self._serializer))
        return result

    def set_types(self, serializer1, serializer2):
        tuple_serializer = TupleSerializer()
        tuple_serializer.set_types(serializer1, serializer2)
        self._serializer = ArraySerializer()
        self._serializer.set_type(tuple_serializer)


class DirectoryEntrySerializer(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "DirectoryEntry"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        from nanome.util import DirectoryEntry
        result = DirectoryEntry()
        result.name = context.read_using_serializer(self.__string)
        result.is_directory = context.read_bool()
        return result


class FileDataSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "FileData"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        from nanome.util import FileErrorCode, FileData
        result = FileData()
        count = context.read_int()
        result.data = context.read_bytes(count)
        result.error_code = FileErrorCode(context.read_int())
        return result


class FileSaveDataSerializer(TypeSerializer):
    def __init__(self):
        self.__string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "FileSaveData"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value.path)
        context.write_int(len(value.data))
        context.write_bytes(value.data)

    def deserialize(self, version, context):
        from nanome.util import FileErrorCode, FileSaveData
        result = FileSaveData()
        result.path = context.read_using_serializer(self.__string)
        result.error_code = FileErrorCode(context.read_int())
        return result


class IntSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "int"

    def serialize(self, version, value, context):
        context.write_int(value)

    def deserialize(self, version, context):
        return context.read_int()


class LongSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "long"

    def serialize(self, version, value, context):
        context.write_long(value)

    def deserialize(self, version, context):
        return context.read_long()


class QuaternionSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "Quaternion"

    def serialize(self, version, value, context):
        context.write_float(value._x)
        context.write_float(value._y)
        context.write_float(value._z)
        context.write_float(value._w)

    def deserialize(self, version, context):
        from nanome.util import Quaternion
        quaternion = Quaternion()
        x = context.read_float()
        y = context.read_float()
        z = context.read_float()
        w = context.read_float()
        quaternion.set(x, y, z, w)
        return quaternion


class UnityRotationSerializer(TypeSerializer):
    def __init__(self):
        self._Quat = QuaternionSerializer()

    def version(self):
        return 0

    def name(self):
        return "UnityRotation"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._Quat, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self._Quat)


class StringSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "string"

    def serialize(self, version, value, context):
        to_write = to_bytes(value, 'utf-8')
        context.write_uint(len(to_write))
        context.write_bytes(to_write)

    def deserialize(self, version, context):
        count = context.read_uint()
        bytes = context.read_bytes(count)
        str = bytes.decode("utf-8")
        return str


class TupleSerializer(TypeSerializer):
    def __init__(self, serializer1=None, serializer2=None):
        self._serializer1 = serializer1
        self._serializer2 = serializer2

    def version(self):
        return 0

    def name(self):
        return "Tuple"

    def serialize(self, version, value, context):
        if self._serializer1 == None or self._serializer2 == None:
            raise TypeError(
                'Trying to serialize tuple without setting content type first')
        (first, second) = value
        context.write_using_serializer(self._serializer1, first)
        context.write_using_serializer(self._serializer2, second)

    def deserialize(self, version, context):
        if self._serializer1 == None or self._serializer2 == None:
            raise TypeError(
                'Trying to deserialize tuple without setting content type first')
        first = context.read_using_serializer(self._serializer1)
        second = context.read_using_serializer(self._serializer2)
        return (first, second)

    def set_types(self, serializer1, serializer2):
        self._serializer1 = serializer1
        self._serializer2 = serializer2


class Vector3Serializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "Vector3"

    def serialize(self, version, value, context):
        context.write_float(value.x)
        context.write_float(value.y)
        context.write_float(value.z)

    def deserialize(self, version, context):
        from nanome.util import Vector3
        x = context.read_float()
        y = context.read_float()
        z = context.read_float()
        return Vector3(x, y, z)


class UnityPositionSerializer(TypeSerializer):
    def __init__(self):
        self._vec3 = Vector3Serializer()

    def version(self):
        return 0

    def name(self):
        return "UnityPosition"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._vec3, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self._vec3)
