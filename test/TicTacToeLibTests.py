import unittest
import TicTacToeLib


class TicTacToeLibTests(unittest.TestCase):

    def setUp(self):
        self.blanktestboard=[TicTacToeLib.BLANK]*TicTacToeLib.GAME_BOARD_SIZE
        self.board=TicTacToeLib.Board()
        self.player=TicTacToeLib.Player('X')

    # Board.getGameBoard()
    def testGetGameBoard(self):
        self.assertEqual(self.blanktestboard, self.board.getGameBoard())
        
    def testGetGameBoardFalse(self):
        self.blanktestboard[0]='X'
        self.assertNotEqual(self.blanktestboard, self.board.getGameBoard())
    
    # Board.__isValidMove    
    def testIsValidMove(self):
        # ugly but I don't need this exposed
        self.assertTrue(self.board._Board__isValidMove(0))

    def testIsValidMoveFalse(self):
        # ugly but I don't need this exposed
        self.board._Board__gameboard[0]='X'
        # self.board.move(self.player,0)
        self.assertFalse(self.board._Board__isValidMove(0))
    
    # Board.move()     
    def testMove(self):
        self.assertTrue(self.board.move(self.player,0))
        
    def testMoveFalse(self):
        self.board._Board__gameboard[0]='X'
        self.assertFalse(self.board.move(self.player,0))
    
    # Board.move() + Board.getGameBoard()    
    def testMoveMadeNE(self):
        self.board.move(self.player,0)
        self.assertNotEqual(self.blanktestboard, self.board.getGameBoard())
        
    def testMoveMadeEQ(self):
        self.blanktestboard[0] = 'X'
        self.board.move(self.player,0)
        self.assertEqual(self.blanktestboard, self.board.getGameBoard()) 
    
    #Player.__init__() tests    
    def testPlayer(self):
        self.assertTrue(self.player.piece == 'X')
    
    def testPlayerFalse(self):
        self.assertFalse(self.player.piece != 'X')


if __name__ == "__main__":
    unittest.main()

