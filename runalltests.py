import unittest
from JudgeTest import JudgeTest
from BoardTest import BoardTest
suite1 = unittest.TestLoader().loadTestsFromTestCase(JudgeTest)
suite2 = unittest.TestLoader().loadTestsFromTestCase(BoardTest)

tests = [suite1, suite2]
alltests = unittest.TestSuite(tests)
unittest.TextTestRunner(verbosity=2).run(alltests)
