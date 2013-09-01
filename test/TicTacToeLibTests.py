import unittest
import TicTacToeLib


class TicTacToeLibTests(unittest.TestCase):

    def setUp(self):
        self.blanktestboard=[TicTacToeLib.BLANK]*TicTacToeLib.GAME_BOARD_SIZE
        self.board=TicTacToeLib.Board()
        self.player=TicTacToeLib.Player('X')

    def testGetBoard(self):
        self.assertEqual(self.blanktestboard, self.board.getGameBoard())
        
    def testGetBoardFalse(self):
        self.blanktestboard[0]='X'
        self.assertNotEqual(self.blanktestboard, self.board.getGameBoard())
        
    def testIsValidMove(self):
        # ugly but I don't need this exposed
        self.assertTrue(self.board._Board__isValidMove(0))

    # TODO Need to add a Board.move() to make the next test cleaner 
    def testIsValidMoveFalse(self):
        # ugly but I don't need this exposed
        #self.board._Board__gameboard[0]='X'
        self.board.move(self.player,0)
        self.assertFalse(self.board._Board__isValidMove(0))
        
    def testMove(self):
        self.blanktestboard[0]='X'
        self.assertTrue(self.board.move(self.player,0))
        
    def testMoveMade(self):
        self.board.move(self.player,0)
        self.assertNotEqual(self.blanktestboard, self.board.getGameBoard()) 
        
    def testPlayer(self):
        self.assertTrue(self.player.piece == 'X')
    
    def testPlayerFalse(self):
        self.assertFalse(self.player.piece != 'X')


if __name__ == "__main__":
    unittest.main()

