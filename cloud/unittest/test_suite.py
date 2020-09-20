"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
import unittest
import backlogAPI_test
import bookingAPI_test
import carAPI_test
import customerAPI_test
import locationAPI_test
import staffAPI_test
import api_test

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(backlogAPI_test))
suite.addTests(loader.loadTestsFromModule(bookingAPI_test))
suite.addTests(loader.loadTestsFromModule(carAPI_test))
suite.addTests(loader.loadTestsFromModule(customerAPI_test))
suite.addTests(loader.loadTestsFromModule(locationAPI_test))
suite.addTests(loader.loadTestsFromModule(staffAPI_test))
suite.addTests(loader.loadTestsFromModule(api_test))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)