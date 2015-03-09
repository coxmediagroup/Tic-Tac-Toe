import unittest
import urllib.request
import json

class TestSequenceFunctions(unittest.TestCase):

    def _evalBoard(self, board):
        url = "http://localhost:9000/evalBoard?board=%s"%board
        f = urllib.request.urlopen(url)
        contents = f.read().decode('utf-8')
        f.close()
        return json.loads(contents)

    def test_evalBoard_firstMove(self):
        results = self._evalBoard("X--------")
        self.assertEqual(results['board'], "XO-------")
        self.assertEqual(results['status'], "continue")

    def test_evalBoard_aiWins(self):
        """ From this board...
                XOX
                OOX
                X--
            ...AI should return this...
                XOX
                OOX
                XO-
            ...with status of "iwin"
        """
        results = self._evalBoard("XOXOOXX--")
        self.assertEqual(results['board'], "XOXOOXXO-")
        self.assertEqual(results['status'], "iwin")

if __name__ == '__main__':
    unittest.main()
