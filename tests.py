import unittest
from nanome.util import Logs

import sys

test_directory = 'testing/'
file_pattern = '*_tests.py'

Logs._set_verbose(True)

suite = unittest.TestLoader().discover(test_directory, pattern=file_pattern)
runner = unittest.TextTestRunner(verbosity=1).run(suite)

exit_code = 0 if runner.wasSuccessful() else 1
sys.exit(exit_code)
