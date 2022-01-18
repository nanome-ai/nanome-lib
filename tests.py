import unittest

import sys

test_directory = 'testing/'
file_pattern = '*_tests.py'

suite = unittest.TestLoader().discover(test_directory, pattern=file_pattern)
runner = unittest.TextTestRunner(verbosity=1).run(suite)

exit_code = 0 if runner.wasSuccessful() else 1
sys.exit(exit_code)
