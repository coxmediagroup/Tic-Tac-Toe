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

def TestWin():
	global comp

	#this should produce a cat
	a = '[{"1":2, "2":2, "3":1, "4":1, "5":2, "6":2, "7":2, "8":1, "9":1}]'

	matrix = json.loads(a)[0]
	# print a
	return comp.check_for_win(matrix)

# Here's our "unit tests".
class aiTests(unittest.TestCase):

    def testRandGen(self):
        self.failUnless(TestGen(9))

    def testWin(self):
    	self.failUnless(TestWin() is None)

def main():
    unittest.main()

if __name__ == '__main__':
    main()