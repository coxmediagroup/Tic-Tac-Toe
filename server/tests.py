import unittest

from google.appengine.ext import testbed


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def testSomething(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
