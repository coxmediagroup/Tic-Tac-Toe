import unittest
import random
import board
import minimax
import movecache

class BoardTest(unittest.TestCase):

    def setUp(self):
        self.board = board.Board()

    def test_initial_empty(self):
        for row in self.board.board:
            for position in row:
                self.assertEqual(position, board.EMPTY_MARKER)

    def test_move_marks_board(self):
        self.board.move('X', 0, 0)
        self.assertEqual(self.board.board[0][0], 'X')
        self.board.move('O', 1, 0)
        self.assertEqual(self.board.board[0][1], 'O')

    def test_out_of_bounds_move_rejected(self):
        self.assertRaises(IndexError, self.board.move, 'X',-1,0)
        self.assertRaises(IndexError, self.board.move, 'X', 3,0)

    def test_occupied_move_rejected(self):
        self.board.move('X', 0, 0)
        self.assertRaises(ValueError, self.board.move, 'O', 0, 0)

    def test_empty_squares(self):
        expectedAvailable = [(x,y) for x in range(3) for y in range(3)]
        self.assertEqual(self.board.getEmptySquares(), expectedAvailable)
        while len(expectedAvailable) > 0:
            position = expectedAvailable.pop()
            self.board.move('X', position[0], position[1])
            self.assertEqual(self.board.getEmptySquares(), expectedAvailable)

    def test_finished(self):
        self.assertEqual(self.board.finished(),(False, None))
        #horizontal win
        self.board.move('X', 0, 0)
        self.board.move('X', 1, 0)
        self.board.move('X', 2, 0)
        self.assertEqual(self.board.finished(), (True, 'X'))
        self.board.reset()
        #vertical win
        self.board.move('O', 0, 0)
        self.board.move('O', 0, 1)
        self.board.move('O', 0, 2)
        self.assertEqual(self.board.finished(), (True, 'O'))
        self.board.reset()
        #diagonal wins
        self.board.move('X', 0, 0)
        self.board.move('X', 1, 1)
        self.board.move('X', 2, 2)
        self.assertEqual(self.board.finished(), (True, 'X'))
        self.board.reset()
        self.board.move('O', 2, 0)
        self.board.move('O', 1, 1)
        self.board.move('O', 0, 2)
        self.assertEqual(self.board.finished(), (True, 'O'))
        #tie
        self.board.reset()
        self.board.move('O', 0, 0)
        self.board.move('X', 0, 1)
        self.board.move('X', 1, 0)
        self.board.move('O', 1, 1)
        self.board.move('O', 0, 2)
        self.board.move('O', 1, 2)
        self.board.move('X', 2, 2)
        self.board.move('O', 2, 1)
        self.board.move('X', 2, 0)
        self.assertEqual(self.board.finished(), (True, None))



class MinimaxTest(unittest.TestCase):
    #I can't think of a lot of ways to test minimax thoroughly

    def setUp(self):
        self.board = board.Board()
        self.calc = minimax.MinimaxCalculator()

    def test_trivial_wins(self):
        self.board.move('X', 1, 1)
        self.board.move('O', 0, 1)
        self.board.move('X', 0, 2)
        self.board.move('O', 0, 0)#O, you're such an idiot
        bestMove = self.calc.bestMove('X', self.board)
        self.assertEqual(bestMove, (2,0))
        self.board.reset()
        self.board.move('X',1,1)
        self.board.move('O',0,0)
        self.board.move('X',2,0)
        self.board.move('O',0,2)
        self.board.move('X',2,1)#X, you so stupid
        bestMove = self.calc.bestMove('O', self.board)
        self.assertEqual(bestMove, (0,1))

    def test_blocks(self):#if it's unbeatable, it must always block
        self.board.move('X', 1, 1)
        self.board.move('O', 0, 0)
        self.board.move('X', 0, 2)
        bestMove = self.calc.bestMove('O', self.board)
        self.assertEqual(bestMove, (2, 0))
        self.board.move('O', 2, 0)
        bestMove = self.calc.bestMove('X', self.board)
        self.assertEqual(bestMove, (1, 0))

    def test_minimax_against_itself(self):#if it's actually perfect, it will always tie itself
        players = ['X', 'O']
        for gameNum in range(100):
            moveNum = 1
            self.board.move('X', random.randint(0,2), random.randint(0,2))
            while not self.board.finished()[0]:
                move = self.calc.bestMove(players[moveNum%2], self.board)
                self.board.move(players[moveNum%2], move[0], move[1])
                moveNum+=1
            self.assertEqual(self.board.finished()[1], None)
            self.board.reset()


class MoveCacheTest(unittest.TestCase):
    
    def setUp(self):
        self.cache = movecache.MoveCache(collectionName='testCollection')
        self.board = board.Board()

    def test_basic_create_and_read(self):
        boardHash = self.board.boardHash()
        document = {'foo':24}
        self.cache[boardHash] = document
        retrievedDocument = self.cache[boardHash]
        self.assertEqual(retrievedDocument['foo'], document['foo'])    

    def test_same_board_gets_same_document(self):
        newBoard = board.Board()
        self.board.move('X', 1,1)
        newBoard.move('X', 1, 1)
        self.board.move('O', 0, 0)
        newBoard.move('O', 0, 0)
        document = {'foo': 2}
        self.cache[self.board.boardHash()] = document
        self.assertEqual(self.cache[self.board.boardHash()], self.cache[newBoard.boardHash()])

    def test_invalid_read_throws_keyerror(self):
        def tryIdx(idx):
            return self.cache[idx]
        self.assertRaises(KeyError,tryIdx, self.board.boardHash())

    def test_update(self):
        document = {'foo': 42, 'bat':'baz'}
        self.cache[self.board.boardHash()] = document
        del document['bat']
        document['bar'] = 'Magrathea'
        self.cache[self.board.boardHash()] = document
        retrievedDocument = self.cache[self.board.boardHash()]
        self.assertEqual(document['foo'], retrievedDocument['foo'])
        self.assertEqual(document['bar'], retrievedDocument['bar'])
        if 'bat' in retrievedDocument:
            self.fail()

    def test_get_returns_default_on_nonexistant(self):
        retrieved = self.cache.get(self.board.boardHash(), 'default')
        self.assertEqual(retrieved, 'default')

    def test_get_returns_document_on_existing(self):
        document={'foo':123}
        self.cache[self.board.boardHash()] = document
        retrieved = self.cache.get(self.board.boardHash(), None)
        self.assertEqual(retrieved['foo'], document['foo'])

    def tearDown(self):
        self.board.reset()
        self.cache.clear()


class MongoMinimaxTest(unittest.TestCase):
    
    def setUp(self):
        self.cache = movecache.MoveCache(collectionName='minimaxTestCollection')
        self.board = board.Board()
        self.calc = minimax.MinimaxCalculator(self.cache)

    def test_minimax_against_itself(self):#pretty sure this'll adequately test the pair
        players = ['X', 'O']
        for gameNum in range(100):
            moveNum = 1
            self.board.move('X', random.randint(0,2), random.randint(0,2))
            while not self.board.finished()[0]:
                move = self.calc.bestMove(players[moveNum%2], self.board)
                self.board.move(players[moveNum%2], move[0], move[1])
                moveNum+=1
            self.assertEqual(self.board.finished()[1], None)
            self.board.reset()





if __name__ == "__main__":
    unittest.main()
