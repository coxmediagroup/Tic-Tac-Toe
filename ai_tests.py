import unittest
import ai
import json

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
	a = '[{"1":2, "2":2, "3":0, "4":1, "5":2, "6":1, "7":0, "8":1, "9":1}]'
	matrix = json.loads(a)[0]
	# print a
	return comp.check_for_win(matrix)

# Here's our "unit tests".
class aiTests(unittest.TestCase):

    def testRandGen(self):
        self.failUnless(TestGen(9))

    def testCounter(self):
    	self.failUnless(TestCounter() is None)

    def testWin(self):
    	self.failUnless(TestWin() is None)

def main():
    unittest.main()

if __name__ == '__main__':
    main()