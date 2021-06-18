import unittest

test_directory = 'testing/'
file_pattern = '*_tests.py'

suite = unittest.TestLoader().discover(test_directory, pattern=file_pattern)
unittest.TextTestRunner(verbosity=2).run(suite)
