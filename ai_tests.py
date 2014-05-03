import unittest
import ai

# Here's our "unit".

gen = ai.gen()
comp = ai.comp()

def TestGen(n):
	global gen
	rand = gen.rand(n)
	return rand

def TestCounter():
	global comp
	return comp.check_for_counter()

def TestWin():
	global comp
	return comp.check_for_win()

# Here's our "unit tests".
class aiTests(unittest.TestCase):

    def testRandGen(self):
        self.failUnless(TestGen(9))

    def testAI(self):
    	self.failUnless(TestCounter() is None)

    def testAI(self):
    	self.failUnless(TestWin() is None)

def main():
    unittest.main()

if __name__ == '__main__':
    main()