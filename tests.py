from testing import atom_tests
from testing import mmcif_tests
from testing import sdf_tests
from testing import ui_tests
from testing import json_tests
from testing import api_tests
from testing import context_tests
from testing import utilities as util

import os

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
if not os.path.isdir(test_output_dir):
    os.makedirs(test_output_dir)

import os

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

import nanome
from nanome.util import Logs
Logs._set_verbose(True)
all_tests_passed = True
all_tests_passed = all_tests_passed and util.run_test_group(context_tests)
all_tests_passed = all_tests_passed and util.run_test_group(api_tests)
all_tests_passed = all_tests_passed and util.run_test_group(atom_tests)
all_tests_passed = all_tests_passed and util.run_test_group(mmcif_tests)
all_tests_passed = all_tests_passed and util.run_test_group(sdf_tests)
all_tests_passed = all_tests_passed and util.run_test_group(ui_tests)
all_tests_passed = all_tests_passed and util.run_test_group(json_tests)
assert(all_tests_passed)