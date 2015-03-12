import unittest
import urllib.request
import json

AI_VS_AI_GAMES = 3
AI_VS_RANDOM_GAMES = 25

class TestSequenceFunctions(unittest.TestCase):

    def _evalBoard(self, board):
        url = "http://localhost:9000/evalBoard?board=%s"%board
        f = urllib.request.urlopen(url)
        contents = f.read().decode('utf-8')
        f.close()
        return json.loads(contents)

    def test_evalBoard_firstMove(self):
        results = self._evalBoard("X--------")
        self.assertEqual(results['status'], "continue")
        self.assertEqual(results['positions'], [])

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
               and positions of [1,4,7]
        """
        results = self._evalBoard("XOXOOXX--")
        self.assertEqual(results['board'], "XOXOOXXO-")
        self.assertEqual(results['status'], "iwin")
        self.assertEqual(results['positions'], [1,4,7])

    def test_evalBoard_humanWins(self):
        """ From this board...
                XOX
                OXO
                X--
            ...AI should return this...
                XOX
                OXO
                X--
            ...with status of "uwin"
               and positions of [2,4,6]
        """
        results = self._evalBoard("XOXOXOX--")
        self.assertEqual(results['board'], "XOXOXOX--")
        self.assertEqual(results['status'], "uwin")
        self.assertEqual(results['positions'], [2,4,6])

    def test_evalBoard_draw(self):
        """ From this board...
                XOX
                XOX
                OXO
            ...AI should return this...
                XOX
                XOX
                OXO
            ...with status of "draw"
               and positions of []
        """
        results = self._evalBoard("XOXXOXOXO")
        self.assertEqual(results['board'], "XOXXOXOXO")
        self.assertEqual(results['status'], "draw")
        self.assertEqual(results['positions'], [])

    def test_evalBoard_aiVSai(self):
        """ Have AI play itself a number of times.
        """
        def swapOsAndXs(board):
            return board.replace('X','~').replace('O','X').replace('~','O')

        games = AI_VS_AI_GAMES
        for n in range(1,games+1):
            print("\nAI vs AI: Game %d of %d"%(n,games))
            board = '---------'
            status = 'continue'
            while status == 'continue':
                # print(board)
                results = self._evalBoard(board)
                board = results['board']
                # print(board)
                board = swapOsAndXs(board)
                status = results['status']
            # print(status)
            self.assertEqual(status, 'draw')

    def test_evalBoard_aiVSrandom(self):
        """ Have AI play random opponent a number of times.
        """
        import random
        def randomMove(board):
            board = list(board)
            emptyPositions = [pos for pos in range(9) if board[pos] == '-']
            movePos = random.choice(emptyPositions)
            board[movePos] = 'X'
            return ''.join(board)

        games = AI_VS_RANDOM_GAMES
        for n in range(1,games+1):
            print("\nAI vs Random: Game %d of %d"%(n,games))
            board = '---------'
            status = 'continue'
            while status == 'continue':
                # print(board)
                board = randomMove(board)
                # print(board)
                results = self._evalBoard(board)
                board = results['board']
                status = results['status']
            # print(status)
            self.assertIn(status, ['iwin', 'draw'])


if __name__ == '__main__':
    unittest.main()
