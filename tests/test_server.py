import configparser
import unittest
import urllib.request
import json

# initialize config
CONFIG = configparser.ConfigParser()
CONFIG.read('server/config.ini')

# initialize URL_PREFIX
_host_name = CONFIG['DEFAULT']['host_name']
_host_port = int(CONFIG['DEFAULT']['host_port'])
if not _host_name: _host_name = 'localhost'
URL_PREFIX = "http://%s:%s/evalBoard?board="%(_host_name, _host_port)

class TestSequenceFunctions(unittest.TestCase):
    def _evalBoard(self, board):
        f = urllib.request.urlopen(URL_PREFIX + board)
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

        print()
        games = int(CONFIG['TESTS']['number_of_ai_vs_ai_games'])
        for n in range(1, games+1):
            print("AI vs AI: Game %d of %d... "%(n, games), end="")
            board = '---------'
            status = 'continue'
            while status == 'continue':
                results = self._evalBoard(board)
                board = results['board']
                board = swapOsAndXs(board)
                status = results['status']
            print(status)
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

        print()
        games = int(CONFIG['TESTS']['number_of_ai_vs_random_games'])
        for n in range(1, games+1):
            print("AI vs Random: Game %d of %d... "%(n, games), end="")
            board = '---------'
            status = 'continue'
            while status == 'continue':
                board = randomMove(board)
                results = self._evalBoard(board)
                board = results['board']
                status = results['status']
            print(status)
            self.assertIn(status, ['iwin', 'draw'])


if __name__ == '__main__':
    unittest.main()
