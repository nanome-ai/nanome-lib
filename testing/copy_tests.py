import nanome
import os

from nanome.api import structure as struct
from testing.utilities import *

from nanome.util import Logs

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
options = TestOptions(ignore_vars=["_unique_identifier"])

alter_object = lambda x: x

def run(counter):
    run_test(test_shallow, counter)
    run_test(test_deep, counter)

#testing structures
def test_shallow():
    shallow_copy_tester(struct.Atom)
    shallow_copy_tester(struct.Bond)
    shallow_copy_tester(struct.Residue)
    shallow_copy_tester(struct.Chain)
    shallow_copy_tester(struct.Molecule)
    shallow_copy_tester(struct.Complex)

def shallow_copy_tester(constructor):
    original = constructor()
    alter_object(original)
    copy = original._shallow_copy()
    assert_equal(original, copy, options)

def test_deep():
    deep_copy_tester(2)
    deep_copy_tester(3)
    deep_copy_tester(4)
    deep_copy_tester(5)

def deep_copy_tester(height):
    original = create_full_tree(height)
    alter_object(original)
    copy = original._deep_copy()
    assert_equal(original, copy, options)

