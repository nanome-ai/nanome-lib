from nanome.util import Logs, Color
import time
import os
import random
import shutil


class TestOptions():
    def __init__(self, ignore_vars=[], accurate_floats=False, print_float_warnings=False):
        self.ignore_vars = ignore_vars
        self.accurate_floats = accurate_floats
        self.print_float_warnings = print_float_warnings


def get_test_assets():
    return os.getcwd() + ("\\testing\\test_assets\\")


def assert_equal(first, second, options=None):
    if (options is None):
        options = TestOptions()
    val, path = verbose_equals(first, second, options)
    if (not val):
        Logs.debug("PATH:")
        Logs.debug("_" * 80)
        for layer in path:
            Logs.debug(layer)
            Logs.debug("_" * 80)
        raise AssertionError


def assert_not_equal(first, second, options=TestOptions()):
    val, path = verbose_equals(first, second, options)
    if (val):
        Logs.debug("All variables equal")
        raise AssertionError


def verbose_equals(first, second, options=TestOptions()):
    return compare_values(first, second, {}, options)


def previously_evaluated(first, second, seen_cache):
    # prevents infinite recursion by caching the results of things already seen.
    # values in cache have already been evaluated or are currently being evaluated.
    if first in seen_cache:
        if second in seen_cache[first]:
            return True
        seen_cache[first].append(second)
    else:
        seen_cache[first] = [second]
    if second in seen_cache:
        if first in seen_cache[second]:
            return True
        seen_cache[second].append(first)
    else:
        seen_cache[second] = [first]
    return False


def compare_values(first, second, seen_cache, options=TestOptions()):
    if first == second:
        return True, []
    # split by type to determing how to compare.
    curr_type = ("type: " + str(first.__class__))
    if not isinstance(second, first.__class__):
        output = [("DeepEqualsError:")]
        output[0] += ("\nfirst type: " + str(first.__class__))
        output[0] += ("\nsecond type: " + str(second.__class__))
        return False, output
    elif isinstance(first, list):
        result, output = compare_lists(first, second, seen_cache, options)
        output.insert(0, curr_type)
        return result, output
    elif isinstance(first, dict):
        result, output = compare_dicts(first, second, seen_cache, options)
        output.insert(0, curr_type)
        return result, output
    else:
        try:
            first_dict = first.__dict__
            second_dict = second.__dict__
        except:
            diff = False
            if isinstance(first, float) and not options.accurate_floats:
                if (abs(first - second) > .00001):
                    diff = True
                elif first != second and options.print_float_warnings:
                    Logs.debug("floating point variables slightly different")
            elif first != second:
                diff = True
            if diff:
                output = [("DeepEqualsError: " + str(first.__class__))]
                output[0] += ("\nfirst val: " + str(first))
                output[0] += ("\nsecond val: " + str(second))
                return False, output
            else:
                return True, []
        else:
            try:
                if previously_evaluated(first, second, seen_cache):
                    return True, []
            except TypeError:  # If type is unhashable
                pass
            result, output = compare_values(first_dict, second_dict, seen_cache, options)
            output.insert(0, curr_type)
            return result, output


def compare_lists(first, second, seen_cache, options=TestOptions()):
    first_len = len(first)
    if first_len != len(second):
        output = [("Lists different lengths")]
        output[0] += ("\nList1 len: " + str(first_len))
        output[0] += ("\nList2 len: " + str(len(second)))

        return False, output
    else:
        for i in range(first_len):
            result, output = compare_values(first[i], second[i], seen_cache, options)
            if result is False:
                return False, output
    return True, []


def compare_dicts(first, second, seen_cache, options=TestOptions()):
    for key in second:
        if isinstance(key, str):
            if key in options.ignore_vars:
                continue
        if (key not in first):
            output = [("DeepEqualsError: " + str(first.__class__))]
            output[0] += ("\nkey " + str(key) + " not in first object")
            return False, output
    for key in first:
        if isinstance(key, str):
            if key in options.ignore_vars:
                continue
        if (key not in second):
            output = [("DeepEqualsError: " + str(first.__class__))]
            output[0] += ("\nkey " + str(key) + " not in second object")
            return False, output
        else:
            result, output = compare_values(first[key], second[key], seen_cache, options)
            if not result:
                # newstr = ("type: " + str(first.__class__))
                newstr = ("\nvariable: " + str(key))
                output.insert(0, newstr)
                return False, output
    return True, []


def alter_object(target, seen_cache={}):
    if previously_altered(target, seen_cache):
        return target
    obj_dict = target.__dict__
    for key, var in obj_dict.items():
        obj_dict[key] = alter_value(var, seen_cache)
    return target


def alter_value(value, seen_cache={}):
    if isinstance(value, list):
        for i in range(len(value)):
            value[i] = alter_value(value[i], seen_cache)
        return value
    elif isinstance(value, dict):
        for key, var in value.items():
            value[key] = alter_value(var, seen_cache)
        return value
    else:
        try:
            value = alter_object(value, seen_cache)
            return value
        except:
            if isinstance(value, bool):
                return not value
            elif isinstance(value, int):
                if (value == 4294967295):
                    value = 1
                return value + 1
            elif isinstance(value, str):
                return value + " altered"
            elif isinstance(value, float):
                return value + .1
            else:
                return value


def previously_altered(value, seen_cache):
    # prevents infinite recursion by caching the results of things already seen.
    # values in cache have already been evaluated or are currently being evaluated.
    if value in seen_cache:
        return True
    else:
        seen_cache[value] = True
    return False


def test_serializer(serializer, obj_to_test, options=None):
    from nanome._internal._network._serialization._context import _ContextDeserialization, _ContextSerialization
    context_s = _ContextSerialization(plugin_id=random.randint(0, 0xFFFFFFFF), version_table=FakeVersionTable())
    serializer.serialize(serializer.version(), obj_to_test, context_s)
    context_d = _ContextDeserialization(context_s.to_array(), FakeVersionTable())
    result = serializer.deserialize(serializer.version(), context_d)
    assert_equal(obj_to_test, result, options)


class FakeVersionTable(object):
    def __getitem__(self, key):
        return 2 ^ 32


def create_test(name, func, args):
    def test():
        return func(*args)
    test.__name__ = name
    return test


def create_full_tree(height):
    from nanome import structure as struct
    if height == 1:
        atom = alter_object(struct.Atom())
        return atom
    if height == 2:
        residue = alter_object(struct.Residue())
        for i in range(3):
            atom = create_full_tree(height - 1)
            atom.name = "atom" + str(i)
            residue.add_atom(atom)
        bond_atoms(residue._atoms[0], residue._atoms[1])
        bond_atoms(residue._atoms[1], residue._atoms[2])
        return residue
    if height == 3:
        chain = alter_object(struct.Chain())
        for i in range(3):
            residue = create_full_tree(height - 1)
            residue.name = "residue" + str(i)
            residue.serial = i + 1
            chain.add_residue(residue)
        bond_atoms(chain._residues[0]._atoms[0], chain._residues[1]._atoms[1])
        bond_atoms(chain._residues[0]._atoms[1], chain._residues[1]._atoms[2])
        return chain
    if height == 4:
        molecule = alter_object(create_molecule())
        for i in range(3):
            chain = create_full_tree(height - 1)
            chain.name = "chain" + str(i)
            molecule.add_chain(chain)
        bond_atoms(molecule._chains[0]._residues[0]._atoms[0], molecule._chains[1]._residues[1]._atoms[1])
        bond_atoms(molecule._chains[0]._residues[0]._atoms[1], molecule._chains[1]._residues[1]._atoms[2])
        return molecule
    if height == 5:
        complex = alter_object(create_complex())
        for i in range(3):
            molecule = create_full_tree(height - 1)
            molecule.name = "molecule" + str(i)
            complex.add_molecule(molecule)
        return complex


def create_molecule():
    from nanome import structure as struct
    molecule = struct.Molecule()
    molecule._associateds = [
        {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
            "key4": "value4",
        }
    ]
    return molecule


def create_complex():
    from nanome import structure as struct
    complex = struct.Complex()
    complex._remarks = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "key4": "value4",
    }
    return complex


def bond_atoms(atom1, atom2):
    from nanome import structure as struct
    bond = struct.Bond()
    bond.atom1 = atom1
    bond.atom2 = atom2
    atom1.residue._add_bond(bond)
    return alter_object(bond)


def rand_int(min=-0x7FFFFFFF, max=0x7FFFFFFF):
    return random.randint(min, max)


def rand_float(min=-340282346638528859811704183484516925440, max=340282346638528859811704183484516925440):
    import struct
    dbl = random.uniform(min, max)
    flt = struct.unpack('f', struct.pack('f', dbl))[0]
    return flt


def rand_positive_long(min=0x7FFFFFFF, max=0x7FFFFFFFFFFFFFFF):
    return random.randint(min, max)


def rand_negative_long(min=-0x7FFFFFFFFFFFFFFF, max=-0x7FFFFFFF):
    return random.randint(min, max)


def rand_uint(min=0x00000000, max=0xFFFFFFFF):
    return random.randint(min, max)


def rand_byte(min=0x00, max=0xFF):
    return random.randint(min, max)


def rand_string():
    return str(rand_int())


def rand_color():
    return Color(whole_num=rand_int())


class Counter():
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def read(self):
        return self.count

    def reset(self):
        self.count = 0

    def to_string(self):
        return "counter(" + self.count + ")"


class DebugTimer():

    _name_space = 30
    _elapsed_space = 14
    _percent_space = 10
    _process_total_space = 14

    @classmethod
    def start_process(cls, name):
        new_process = cls.Process(name)
        if cls.curr_process is not None:
            cls.curr_process._add_child(new_process)
        cls.curr_process = new_process
        cls.curr_process = new_process
        return new_process

    @classmethod
    def close_proces(cls):
        cls.curr_process.close()

    @classmethod
    def clear(cls):
        cls._start()

    @classmethod
    def _process_closed(cls, process):
        if process != cls.curr_process:
            Logs.error("Timer process closed out of order.")
        cls.curr_process = process._parent

    @classmethod
    def summary(cls):
        return cls.curr_process.summary()

    class Process():
        def __init__(self, name):
            self.name = name
            self.start_time = DebugTimer._get_time()
            self.close_time = None
            self._children = []
            self._parent = None
            self.note = ""
            self.show_once = False
            self.hide = {}

        @property
        def elapsed_time(self):
            if self.close_time is not None:
                return self.close_time - self.start_time
            return DebugTimer._get_time() - self.start_time

        def _add_child(self, other):
            other._parent = self
            self._children.append(other)

        def close(self):
            self.close_time = DebugTimer._get_time()
            DebugTimer._process_closed(self)
            if self.name not in DebugTimer.process_totals:
                DebugTimer.process_totals[self.name] = 0
            DebugTimer.process_totals[self.name] += self.elapsed_time

        def summary(self):
            line_counter = Counter()
            header = self._get_line("#", "Name", "Elapsed", "Percent", "Cumulative", "Note", 0)
            total_time = self.elapsed_time
            lines = [header]
            self._summary(0, total_time, lines, line_counter)
            return "".join(lines)

        def _summary(self, depth, total_time, lines, line_counter):
            if self._parent and self.name in self._parent.hide:
                return lines
            if self._parent and self.show_once:
                self._parent.hide[self.name] = True
            elapsed = self.elapsed_time
            percent = elapsed / total_time * 100
            process_total = DebugTimer.process_totals[self.name]
            line = self._get_line(line_counter.read(), self.name, elapsed, percent, process_total, self.note, depth)
            line_counter.increment()
            lines.append(line)
            for child in self._children:
                child._summary(depth + 1, total_time, lines, line_counter)

        @classmethod
        def _get_line(cls, line_number, name, elapsed, percent, process_total, note, depth):
            _line_number = cls._format_block(line_number, 4, False)
            _tab = "--" * depth
            _name = name
            _elapsed = cls._format_block(elapsed, DebugTimer._elapsed_space)
            _percent = cls._format_block(percent, DebugTimer._percent_space)
            _process_total = cls._format_block(process_total, DebugTimer._process_total_space)
            _note = cls._format_block(note, 40)
            left = "%s|%s|%s" % (_line_number, _tab, _name)
            right = "%s|%s|%s|%s\n" % (_elapsed, _percent, _process_total, _note)
            width = shutil.get_terminal_size().columns
            space = width - len(left) - len(right)
            line = left + ("-" * space) + right
            return line

        @classmethod
        def _format_block(cls, text, size, adjust_left=True):
            buff = cls._left_buffer if adjust_left else cls._right_buffer
            if isinstance(text, float):
                text = str(round(text, 5))
            elif isinstance(text, int):
                text = str(text)
            return buff(str(text), size)[:size]

        @staticmethod
        def _right_buffer(text, length=8):
            text = str(text)
            diff = length - len(text)
            if diff > 0:
                text = " " * diff + text
            return text

        @staticmethod
        def _left_buffer(text, length=8):
            text = str(text)
            diff = length - len(text)
            if diff > 0:
                text = text + " " * diff
            return text

    @classmethod
    def _start(cls):
        cls.nano = 10**9
        cls.milli = 10**3
        cls.curr_process = None
        cls.process_totals = {}

    @classmethod
    def _get_time(cls):
        # return time.clock()
        # return int(time.clock() * cls.nano)
        return time.clock() * cls.milli


DebugTimer._start()
