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
	a = '[{"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0}]'
	matrix = json.loads(a)[0]
	print matrix['3']
	# print a
	return comp.check_for_win()

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