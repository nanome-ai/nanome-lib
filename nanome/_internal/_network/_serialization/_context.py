from .. import _Data
import struct
from nanome.util import Logs

class _PacketDebuggingException(Exception):
	def __init__(self):
		self.__stack = []

	def _append(self, value):
		self.__stack.append(value)

	def _pop(self):
		self.__stack.pop()

	def _raise(self, current_value):
		stack_str = ""
		for value in self.__stack:
			stack_str += value + " -> "
		stack_str += current_value
		super().__init__("Error while trying to deserialize the following : " + stack_str)
		raise self

class _ContextSerialization(object):
    # pylint: disable=method-hidden
    def __init__(self, plugin_id, version_table = None, packet_debugging = False):
        self._data = _Data()
        self.payload = {}
        self.__version_table = version_table
        if packet_debugging:
            self.write_bool = self.write_bool_debug
            self.write_byte = self.write_byte_debug
            self.write_bytes = self.write_bytes_debug
            self.write_float = self.write_float_debug
            self.write_long = self.write_long_debug
            self.write_int = self.write_int_debug
            self.write_uint = self.write_uint_debug
            self.write_using_serializer = self.write_using_serializer_debug
        self.__packet_debugging = packet_debugging
        self._plugin_id = plugin_id

    def has_packet_debugging(self):
        return self.__packet_debugging

    def write_bool(self, value):
        self._data.write_bool(value)

    def write_bool_debug(self, value):
        self._data.write_uint(0xCAFEB001)
        self._data.write_bool(value)

    def write_byte(self, value):
        self._data.write_byte(value)

    def write_byte_debug(self, value):
        self._data.write_uint(0xCAFEB007)
        self._data.write_byte(value)

    def write_bytes(self, value):
        self._data.write_bytes(value)

    def write_bytes_debug(self, value):
        self._data.write_uint(0xCAFEB002)
        self._data.write_bytes(value)

    def write_float(self, value):
        self._data.write_float(value)

    def write_float_debug(self, value):
        self._data.write_uint(0xCAFEB003)
        self._data.write_float(value)

    def write_long(self, value):
        self._data.write_long(value)

    def write_long_debug(self, value):
        self._data.write_uint(0xCAFEB004)
        self._data.write_long(value)

    def write_int(self, value):
        self._data.write_int(value)

    def write_int_debug(self, value):
        self._data.write_uint(0xCAFEB005)
        self._data.write_int(value)

    def write_uint(self, value):
        self._data.write_uint(value)

    def write_uint_debug(self, value):
        self._data.write_uint(0xCAFEB006)
        self._data.write_uint(value)

    def write_byte_array(self, value):
        self._data.write_byte_array(value)

    def write_float_array(self, value):
        self._data.write_float_array(value)

    def write_int_array(self, value):
        self._data.write_int_array(value)

    def write_long_array(self, value):
        self._data.write_long_array(value)

    def write_using_serializer(self, serializer, value):
        try:
            version = self.__version_table[serializer.name()]
        except:
            version = 0
        serializer.serialize(version, value, self)

    def write_using_serializer_debug(self, serializer, value):
        self._data.write_uint(0xCAFECAFE)
        try:
            version = self.__version_table[serializer.name()]
        except:
            version = 0
        serializer.serialize(version, value, self)

    def to_array(self):
        return self._data.to_array()

    def get_version_table(self):
        return self.__version_table

    def get_packet_debugging(self):
        return self.__packet_debugging

    def create_sub_context(self):
        sub_context = _ContextSerialization(self._plugin_id, self.__version_table, self.__packet_debugging)
        return sub_context

class _ContextDeserialization(object):
    # pylint: disable=method-hidden
    def __init__(self, bytes, version_table = None, packet_debugging = False):
        self._data = _Data()
        self._data.received_data(bytes)
        self.payload = {}
        self.__version_table = version_table
        if packet_debugging:
            self.__packet_debugging_exception = _PacketDebuggingException()
            self.read_bool = self.read_bool_debug
            self.read_byte = self.read_byte_debug
            self.read_bytes = self.read_bytes_debug
            self.read_float = self.read_float_debug
            self.read_long = self.read_long_debug
            self.read_int = self.read_int_debug
            self.read_uint = self.read_uint_debug
            self.read_using_serializer = self.read_using_serializer_debug
        self.__packet_debugging = packet_debugging

    def has_packet_debugging(self):
        return self.__packet_debugging

    def read_bool(self):
        return self._data.read_bool()

    def read_bool_debug(self):
        debug_flag = self._data.read_uint()
        if debug_flag != 0xCAFEB001:
            self.__packet_debugging_exception._raise("bool")
        return self._data.read_bool()

    def read_byte(self):
        return self._data.read_byte()

    def read_byte_debug(self):
        debug_flag = self._data.read_uint()
        if debug_flag != 0xCAFEB007:
            self.__packet_debugging_exception._raise("byte")
        return self._data.read_byte()

    def read_bytes(self, count):
        return self._data.read_bytes(count)

    def read_bytes_debug(self, count):
        debug_flag = self._data.read_uint()
        if debug_flag != 0xCAFEB002:
            self.__packet_debugging_exception._raise("bytes")
        return self._data.read_bytes(count)

    def read_float(self):
        return self._data.read_float()

    def read_float_debug(self):
        debug_flag = self._data.read_uint()
        if debug_flag != 0xCAFEB003:
            self.__packet_debugging_exception._raise("float")
        return self._data.read_float()

    def read_long(self):
        return self._data.read_long()

    def read_long_debug(self):
        debug_flag = self._data.read_uint()
        if debug_flag != 0xCAFEB004:
            self.__packet_debugging_exception._raise("long")
        return self._data.read_long()

    def read_int(self):
        return self._data.read_int()

    def read_int_debug(self):
        debug_flag = self._data.read_uint()
        if debug_flag != 0xCAFEB005:
            self.__packet_debugging_exception._raise("int")
        return self._data.read_int()

    def read_uint(self):
        return self._data.read_uint()

    def read_uint_debug(self):
        debug_flag = self._data.read_uint()
        if debug_flag != 0xCAFEB006:
            self.__packet_debugging_exception._raise("uint")
        return self._data.read_uint()

    def read_int_array(self):
        return self._data.read_int_array()

    def read_byte_array(self):
        return self._data.read_byte_array()

    def read_float_array(self):
        return self._data.read_float_array()

    def read_long_array(self):
        return self._data.read_long_array()

    def read_using_serializer(self, serializer):
        try:
            version = self.__version_table[serializer.name()]
        except:
            version = 0
        return serializer.deserialize(version, self)

    def read_using_serializer_debug(self, serializer):
        debug_flag = self._data.read_uint()
        if debug_flag != 0xCAFECAFE:
            self.__packet_debugging_exception._raise(str(serializer))
        self.__packet_debugging_exception._append(str(serializer))
        try:
            version = self.__version_table[serializer.name()]
        except:
            version = 0
        result = serializer.deserialize(version, self)
        self.__packet_debugging_exception._pop()
        return result

    def get_version_table(self):
        return self.__version_table

    def get_packet_debugging(self):
        return self.__packet_debugging

    def create_sub_context(self):
        return _ContextDeserialization(self.__version_table, self.__packet_debugging)