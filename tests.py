import unittest
from nanome.util import Logs

test_directory = 'testing/'
file_pattern = '*_tests.py'

Logs._set_verbose(True)

suite = unittest.TestLoader().discover(test_directory, pattern=file_pattern)
unittest.TextTestRunner(verbosity=1).run(suite)
