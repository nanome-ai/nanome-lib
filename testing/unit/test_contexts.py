import struct
import random
from nanome._internal._network import _Data
import unittest


def rand_int():
    return random.randint(-0x7FFFFFFF, 0x7FFFFFFF)


def rand_float():
    dbl = random.uniform(-340282346638528859811704183484516925440, 340282346638528859811704183484516925440)
    flt = struct.unpack('f', struct.pack('f', dbl))[0]
    return flt


def rand_positive_long():
    return random.randint(0x7FFFFFFF, 0x7FFFFFFFFFFFFFFF)


def rand_negative_long():
    return random.randint(-0x7FFFFFFFFFFFFFFF, -0x7FFFFFFF)


def rand_uint():
    return random.randint(0x00000000, 0xFFFFFFFF)


def rand_byte():
    return random.randint(0x00, 0xFF)


class ContextTestCase(unittest.TestCase):
    def test_array(self):
        ints_in = []
        for _ in range(1000):
            ints_in.append(rand_int())

        floats_in = []
        for _ in range(1000):
            floats_in.append(rand_float())

        longs_in = []
        for _ in range(1000):
            longs_in.append(rand_positive_long())
            longs_in.append(rand_negative_long())

        buffer = _Data()
        buffer.write_int_array(ints_in)
        buffer.write_float_array(floats_in)
        buffer.write_long_array(longs_in)

        ints_out = buffer.read_int_array()
        floats_out = buffer.read_float_array()
        longs_out = buffer.read_long_array()
        assert(tuple(ints_in) == ints_out)
        assert(tuple(floats_in) == floats_out)
        assert(tuple(longs_in) == longs_out)

    def test_primitive(self):
        buffer = _Data()
        test_values = []
        # bool
        test_values.append(True)
        buffer.write_bool(test_values[-1])
        test_values.append(False)
        buffer.write_bool(test_values[-1])
        # int
        test_values.append(0x7FFFFFFF)  # max signed int
        buffer.write_int(test_values[-1])
        test_values.append(-0x7FFFFFFF)  # min signed int
        buffer.write_int(test_values[-1])
        # single float
        test_values.append(float("inf"))  # float infinity
        buffer.write_float(test_values[-1])
        test_values.append(float("-inf"))  # float infinity
        buffer.write_float(test_values[-1])
        test_values.append(340282346638528859811704183484516925440)  # max float
        buffer.write_float(test_values[-1])
        test_values.append(-340282346638528859811704183484516925440)  # min float
        buffer.write_float(test_values[-1])
        # long
        test_values.append(0x7FFFFFFFFFFFFFFF)  # max long
        buffer.write_long(test_values[-1])
        test_values.append(-0x7FFFFFFFFFFFFFFF)  # min long
        buffer.write_long(test_values[-1])
        # uint
        test_values.append(0xFFFFFFFF)  # max uint
        buffer.write_uint(test_values[-1])
        test_values.append(0x00000000)  # min uint
        buffer.write_uint(test_values[-1])
        # (unsigned) byte
        test_values.append(0xFF)  # max byte
        buffer.write_byte(test_values[-1])
        test_values.append(0x00)  # min byte
        buffer.write_byte(test_values[-1])
        # Randoms
        test_values.append(rand_int())
        buffer.write_int(test_values[-1])
        test_values.append(rand_float())
        buffer.write_float(test_values[-1])
        test_values.append(rand_positive_long())
        buffer.write_long(test_values[-1])
        test_values.append(rand_negative_long())
        buffer.write_long(test_values[-1])
        test_values.append(rand_uint())
        buffer.write_uint(test_values[-1])
        test_values.append(rand_byte())
        buffer.write_byte(test_values[-1])

        # check vals
        i = 0
        assert (buffer.read_bool() == test_values[i])
        i += 1
        assert (buffer.read_bool() == test_values[i])
        i += 1
        assert (buffer.read_int() == test_values[i])
        i += 1
        assert (buffer.read_int() == test_values[i])
        i += 1
        assert (buffer.read_float() == test_values[i])
        i += 1
        assert (buffer.read_float() == test_values[i])
        i += 1
        assert (buffer.read_float() == test_values[i])
        i += 1
        assert (buffer.read_float() == test_values[i])
        i += 1
        assert (buffer.read_long() == test_values[i])
        i += 1
        assert (buffer.read_long() == test_values[i])
        i += 1
        assert (buffer.read_uint() == test_values[i])
        i += 1
        assert (buffer.read_uint() == test_values[i])
        i += 1
        assert (buffer.read_byte() == test_values[i])
        i += 1
        assert (buffer.read_byte() == test_values[i])
        i += 1
        # randoms
        assert (buffer.read_int() == test_values[i])
        i += 1
        assert (buffer.read_float() == test_values[i])
        i += 1
        assert (buffer.read_long() == test_values[i])
        i += 1
        assert (buffer.read_long() == test_values[i])
        i += 1
        assert (buffer.read_uint() == test_values[i])
        i += 1
        assert (buffer.read_byte() == test_values[i])
        i += 1

        # check the buffer is empty
        empty = False
        try:
            buffer.read_byte()
        except:
            empty = True
        assert(empty)
