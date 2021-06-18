import unittest

test_directory = 'testing/'
test_filename = '*_tests.py'


suite = unittest.TestLoader().discover(test_directory, pattern=test_filename)
unittest.TextTestRunner(verbosity=2).run(suite)
