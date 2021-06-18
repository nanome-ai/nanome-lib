import os

from nanome.util import Logs

from testing import utilities as util
from testing import atom_tests
from testing import mmcif_tests
from testing import sdf_tests
from testing import ui_tests
from testing import json_tests
from testing import api_tests
from testing import context_tests
from testing import copy_tests
from testing import conformer_tests
from testing import color_tests


test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
if not os.path.isdir(test_output_dir):
    os.makedirs(test_output_dir)

Logs._set_verbose(True)

all_tests_passed = True
all_tests_passed = all_tests_passed and util.run_test_group(copy_tests)
all_tests_passed = all_tests_passed and util.run_test_group(conformer_tests)
all_tests_passed = all_tests_passed and util.run_test_group(atom_tests)
all_tests_passed = all_tests_passed and util.run_test_group(context_tests)
all_tests_passed = all_tests_passed and util.run_test_group(api_tests)
all_tests_passed = all_tests_passed and util.run_test_group(mmcif_tests)
all_tests_passed = all_tests_passed and util.run_test_group(sdf_tests)
all_tests_passed = all_tests_passed and util.run_test_group(ui_tests)
all_tests_passed = all_tests_passed and util.run_test_group(json_tests)
all_tests_passed = all_tests_passed and util.run_test_group(color_tests)
assert(all_tests_passed)
