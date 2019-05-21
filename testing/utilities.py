from nanome.util import Logs
import time
import traceback

class TestOptions():
    def __init__(self, ignore_vars = [], accurate_floats = False, print_float_warnings = False):
        self.ignore_vars = ignore_vars
        self.accurate_floats = accurate_floats
        self.print_float_warnings = print_float_warnings

def assert_equal(first, second, options = None):
    if (options == None):
        options = TestOptions()
    val, path = verbose_equals(first, second, options)
    if (not val):
        Logs.debug("PATH:")
        Logs.debug("_"*80)
        for layer in path:
            Logs.debug(layer)
            Logs.debug("_"*80)
        raise AssertionError

def assert_not_equal(first, second, options = TestOptions()):
    val, path = verbose_equals(first, second, options)
    if (val):
        Logs.debug("All variables equal")
        raise AssertionError

def verbose_equals(first, second, options = TestOptions()):
    return compare_values(first, second, {}, options)

def previously_evaluated(first, second, seen_cache):
    #prevents infinite recursion by caching the results of things already seen. 
    #values in cache have already been evaluated or are currently being evaluated.
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


def compare_values(first, second, seen_cache, options = TestOptions()):
    if first == second:
        return True, []
    #split by type to determing how to compare.
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
                if (abs(first - second) >.00001):
                    diff = True
                elif first != second and options.print_float_warnings:
                    Logs.debug("floating point variables slightly different")
            elif first != second:
                diff = True
            if diff:
                output = [("DeepEqualsError: " +  str(first.__class__))]
                output[0] += ("\nfirst val: " + str(first))
                output[0] += ("\nsecond val: " + str(second))
                return False, output
            else:
                return True, []
        else:
            if previously_evaluated(first, second, seen_cache):
                return True, []
            result, output = compare_values(first_dict, second_dict, seen_cache, options)
            output.insert(0, curr_type)
            return result, output

def compare_lists(first, second, seen_cache, options = TestOptions()):
    first_len = len(first)
    if first_len != len(second):
        output = [("Lists different lengths")]
        output[0] += ("\nList1 len: " + str(first_len))
        output[0] += ("\nList2 len: " + str(len(second)))

        return False, output
    else:
        for i in range(first_len):
            if not compare_values(first[i], second[i], seen_cache, options):
                output = [("type: " + str(first[i].__class__))]
                output[0] += ("\nindex: " + i)
                return False, []
    return True, []

def compare_dicts(first, second, seen_cache, options = TestOptions()):
    for key in second:
        if isinstance(key, str):
            if key in options.ignore_vars:
                continue
        if (not key in first):
            output = [("DeepEqualsError: " + str(first.__class__))]
            output[0] += ("\nkey "+ str(key) + " not in first object")
            return False, output
    for key in first:
        if isinstance(key, str):
            if key in options.ignore_vars:
                continue
        if (not key in second):
            output = [("DeepEqualsError: " + str(first.__class__))]
            output[0] += ("\nkey " +  str(key) + " not in second object")
            return False, output
        else:
            result, output = compare_values(first[key], second[key], seen_cache, options)
            if not result:
                # newstr = ("type: " + str(first.__class__))
                newstr = ("\nvariable: " + str(key))
                output.insert(0, newstr)
                return False, output
    return True, []

def alter_object(target, seen_cache = {}):
    # if previously_altered(target, seen_cache):
    #     return target
    obj_dict = target.__dict__
    for key, var in obj_dict.items():
        obj_dict[key] = alter_value(var)
    return target

def alter_value(value, seen_cache = {}):
    if isinstance(value, list):
        for i in range(len(value)):
            value[i] = alter_value(value[i], seen_cache)
        return value
    elif isinstance(value, dict):
        for key,var in value.items():
            value[key] = alter_value(var, seen_cache)
        return value
    else:
        try:
            value = alter_object(value, seen_cache = {})
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
    #prevents infinite recursion by caching the results of things already seen. 
    #values in cache have already been evaluated or are currently being evaluated.
    if value in seen_cache:
        return True
    else:
        seen_cache[value] = True
    return False

class TestCounter():
    def __init__(self):
        self.passed = 0 
        self.total = 0 

def run_test_group(test, options = TestOptions()):
    Logs.debug("runnning test group", test.__name__)
    counter = TestCounter()
    test.run(counter)
    Logs.debug("tests passed: ", str(counter.passed)+"/"+str(counter.total))
    if (counter.passed < counter.total):
        return False
    else:
        return True

def run_test(test, counter):
    try:
        Logs.debug("\trunning test", test.__name__)
        counter.total += 1
        test()
    except Exception as err:
        Logs.error("\ttest failed.")
        print(traceback.format_exc())
    else:
        counter.passed += 1

def run_timed_test(test, counter, loop_count = 1, maximum_time = -1.0):
    Logs.debug("\trunning test", test.__name__)
    counter.total += 1    
    timed = True
    try:
        start_time = time.process_time_ns()
    except AttributeError:
        Logs.debug("No timer module. Defaulting to untimed test")
        timed = False
        maximum_time = -1
    try:
        if (timed):
            for _ in range(loop_count):
                test()
            result_time = (time.process_time_ns() - start_time) / 1000000000.0
            Logs.debug("\texecuted in", result_time, "seconds.", result_time/loop_count, "seconds per test.", "Reference time:", maximum_time, "seconds")
        else:
            test()
    except Exception as e:
        Logs.error("\ttest failed.")
        Logs.error(e)
    else:
        if maximum_time >= 0.0 and result_time > maximum_time:
            Logs.error("\ttest successful but too slow")
        else:
            counter.passed += 1

def test_serializer(serializer, obj_to_test, options=None):
    from nanome._internal._network._serialization._context import _ContextDeserialization, _ContextSerialization
    context_s = _ContextSerialization()
    serializer.serialize(serializer.version, obj_to_test, context_s)
    context_d = _ContextDeserialization(context_s.to_array())
    result = serializer.deserialize(serializer.version, context_d)
    assert_equal(obj_to_test, result, options)

def create_test(name, func, args):
    Logs.debug("test: name")
    test = lambda: func(*args)
    test.__name__ = name
    return test