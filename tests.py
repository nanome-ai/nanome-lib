import unittest
from nanome.util import Logs

import sys

test_directory = 'testing/'
file_pattern = '*_tests.py'

Logs._set_verbose(True)

suite = unittest.TestLoader().discover(test_directory, pattern=file_pattern)
runner = unittest.TextTestRunner(verbosity=1).run(suite)

ret = not runner.wasSuccessful()
sys.exit(ret)
