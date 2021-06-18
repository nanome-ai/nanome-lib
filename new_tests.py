import unittest

test_filename = __file__ + '_tests'
test_directory = 'testing'

suite = unittest.TestLoader().discover(test_directory, pattern=test_filename)
unittest.TextTestRunner(verbosity=2).run(suite)
