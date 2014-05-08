import unittest
import ai
import json

# Here's our "unit".
comp = ai.comp()

def TestMove():
	global comp

	#this should produce a cat
	matrix = '{"1":0, "2":0, "3":0, "4":2, "5":1, "6":0, "7":0, "8":1, "9":1}'
	
	results = comp.next_move(matrix)
	print "*************"
	print "Final json output:"
	print results
	print "*************"
	return

# Here's our "unit tests".
class aiTests(unittest.TestCase):

    def testMove(self):
    	self.failUnless(TestMove() is None)

def main():
    unittest.main()

if __name__ == '__main__':
    main()