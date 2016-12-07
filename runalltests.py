import unittest
from JudgeTest import JudgeTest
from BoardTest import BoardTest
from MinMaxTest import MinMaxTest
suite1 = unittest.TestLoader().loadTestsFromTestCase(JudgeTest)
suite2 = unittest.TestLoader().loadTestsFromTestCase(BoardTest)
suite3 = unittest.TestLoader().loadTestsFromTestCase(MinMaxTest)

tests = [suite1, suite2, suite3]
alltests = unittest.TestSuite(tests)
unittest.TextTestRunner(verbosity=2).run(alltests)
