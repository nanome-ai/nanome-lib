import nanome
import os

from nanome.api import structure as struct
from nanome._internal._structure._io import _conformer_helper as conformer
from testing.utilities import *

from nanome.util import Logs

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
options = TestOptions(ignore_vars=["_unique_identifier"])

alter_object = lambda x: x

def run(counter):
    run_test(test_wholistic, counter)

def test_wholistic():
    original = create_full_tree(5)
    alter_object(original)
    copy = conformer.ConvertToConformers(original)
    copy = conformer.ConvertToFrames(copy)
    assert_equal(original, copy, options)
