import struct


class _Data(object):
    bool_pack = struct.Struct('<?').pack_into
    float_pack = struct.Struct('<f').pack_into
    long_pack = struct.Struct('<q').pack_into
    int_pack = struct.Struct('<i').pack_into
    uint_pack = struct.Struct('<I').pack_into

    bool_unpack = struct.Struct('<?').unpack_from
    float_unpack = struct.Struct('<f').unpack_from
    long_unpack = struct.Struct('<q').unpack_from
    int_unpack = struct.Struct('<i').unpack_from
    uint_unpack = struct.Struct('<I').unpack_from

    def __init__(self):
        self._buffered_computed = 0
        self._buffered_bytes = 0
        self._end = 0
        self._received_bytes = bytearray()

    def received_data(self, data):
        start = self._buffered_bytes + self._buffered_computed
        size = len(data)
        self.expand_data(size)
        self._received_bytes[start:start+size] = data

    def expand_data(self, size):
        self._buffered_bytes += size
        if (self._buffered_computed + self._buffered_bytes > self._end):
            self._expand_data(size)

    def _expand_data(self, size):
        expand_size = 1048576 + size
        expand = bytearray(expand_size)
        self._received_bytes.extend(expand)
        self._end += expand_size

    def has_enough(self, size):
        return self._buffered_bytes >= size

    def to_array(self):
        return self._received_bytes[self._buffered_computed:self._buffered_computed+self._buffered_bytes]
        
#region write Data
    def write_bool(self, value):

        pre = self._buffered_bytes + self._buffered_computed
        self.expand_data(1)
        _Data.bool_pack(self._received_bytes, pre, value)

    def write_float(self, value):

        pre = self._buffered_bytes + self._buffered_computed
        self.expand_data(4)
        _Data.float_pack(self._received_bytes, pre, value)

    def write_long(self, value):

        pre = self._buffered_bytes + self._buffered_computed
        self.expand_data(8)
        _Data.long_pack(self._received_bytes, pre, value)

    def write_int(self, value):

        pre = self._buffered_bytes + self._buffered_computed
        self.expand_data(4)
        _Data.int_pack(self._received_bytes, pre, value)

    def write_uint(self, value):

        pre = self._buffered_bytes + self._buffered_computed
        self.expand_data(4)
        _Data.uint_pack(self._received_bytes, pre, value)

    def write_byte(self, value):
        pre = self._buffered_bytes + self._buffered_computed
        self.expand_data(1)
        self._received_bytes[pre] = value

    def write_bytes(self, data):
        pre = self._buffered_bytes + self._buffered_computed
        size = len(data)
        self.expand_data(size)
        self._received_bytes[pre:pre+size] = data
#endregion
#region read Data
    def consume_data(self, size):
        self._buffered_bytes -= size
        self._buffered_computed += size

        if self._buffered_computed > 1048576:
            self._consume_data(size)

    def _consume_data(self, size):
        self._received_bytes = self._received_bytes[self._buffered_computed:]
        self._end -= self._buffered_computed
        self._buffered_computed = 0

    def read_byte(self):
        if self._buffered_bytes == 0:
            raise BufferError(
                'Trying to read more data than available, check API compatibility')
        result = self._received_bytes[self._buffered_computed]
        self.consume_data(1)
        return result

    def read_bytes(self, size):
        # If trying to read an empty payload, return an empty bytearray
        if size == 0:
            return bytearray()

        if self._buffered_bytes == 0 or size > self._buffered_bytes:
            raise BufferError(
                'Trying to read more data than available, check API compatibility')
        result = self._received_bytes[self._buffered_computed:self._buffered_computed + size]
        self.consume_data(size)
        return result

    def read_bool(self):
        pre = self._buffered_computed
        result = _Data.bool_unpack(self._received_bytes, pre)[0]
        self.consume_data(1)
        return result

    def read_float(self):
        pre = self._buffered_computed
        result = _Data.float_unpack(self._received_bytes, pre)[0]
        self.consume_data(4)
        return result

    def read_long(self):
        pre = self._buffered_computed
        result = _Data.long_unpack(self._received_bytes, pre)[0]
        self.consume_data(8)
        return result

    def read_int(self):
        pre = self._buffered_computed
        result = _Data.int_unpack(self._received_bytes, pre)[0]
        self.consume_data(4)
        return result

    def read_uint(self):
        pre = self._buffered_computed
        result = _Data.uint_unpack(self._received_bytes, pre)[0]
        self.consume_data(4)
        return result
#end region
