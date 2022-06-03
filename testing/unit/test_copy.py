import os

from nanome.api import structure as struct
from testing.unit.utilities import alter_object, assert_equal, create_full_tree, TestOptions

import unittest

test_assets = os.getcwd() + ("/testing/test_assets")
options = TestOptions(ignore_vars=["_unique_identifier", "_index", "_alt_loc"])


def shallow_copy_tester(constructor):
    original = constructor()
    alter_object(original)
    copy = original._shallow_copy()
    assert_equal(original, copy, options)


def deep_copy_tester(height):
    original = create_full_tree(height)
    alter_object(original)
    copy = original._deep_copy()
    assert_equal(original, copy, options)


class CopyTestCase(unittest.TestCase):

    def test_shallow(self):
        shallow_copy_tester(struct.Atom)
        shallow_copy_tester(struct.Bond)
        shallow_copy_tester(struct.Residue)
        shallow_copy_tester(struct.Chain)
        shallow_copy_tester(struct.Molecule)
        shallow_copy_tester(struct.Complex)

    def test_deep(self):
        deep_copy_tester(2)
        deep_copy_tester(3)
        deep_copy_tester(4)
        deep_copy_tester(5)
