import unittest
import TicTacToeLib


class TicTacToeLibTests(unittest.TestCase):

    def setUp(self):
        self.blanktestboard=[TicTacToeLib.BLANK]*TicTacToeLib.GAME_BOARD_SIZE
        self.board=TicTacToeLib.Board()
        self.player=TicTacToeLib.Player('X')
        self.player2=TicTacToeLib.Player('O')

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
    
    #Player.__init__()    
    def testPlayer(self):
        self.assertTrue(self.player.piece == 'X')
    
    def testPlayerFalse(self):
        self.assertFalse(self.player.piece != 'X')
        
    #Board.isBoardFull()
    def testIsBoardFullEmptyBoard(self):
        self.assertFalse(self.board.isBoardFull())

    def testIsBoardFullOneMove(self):
        self.board.move(self.player,0)
        self.assertFalse(self.board.isBoardFull())
        
    def testIsBoardFullTwoMoves(self):
        for i in range(2):
            self.board.move(self.player,i)
        self.assertFalse(self.board.isBoardFull())

    def testIsBoardFullThreeMoves(self):
        for i in range(3):
            self.board.move(self.player,i)
        self.assertFalse(self.board.isBoardFull())

    def testIsBoardFullFourMove(self):
        for i in range(4):
            self.board.move(self.player,i)
        self.assertFalse(self.board.isBoardFull())

    def testIsBoardFullFiveMoves(self):
        for i in range(5):
            self.board.move(self.player,i)
        self.assertFalse(self.board.isBoardFull())

    def testIsBoardFullSixMoves(self):
        for i in range(6):
            self.board.move(self.player,i)
        self.assertFalse(self.board.isBoardFull())

    def testIsBoardFullSevenMoves(self):
        for i in range(7):
            self.board.move(self.player,i)
        self.assertFalse(self.board.isBoardFull())

    def testIsBoardFullEightMoves(self):
        for i in range(8):
            self.board.move(self.player,i)
        self.assertFalse(self.board.isBoardFull())

    def testIsBoardFullNineMoves(self):
        for i in range(9):
            self.board.move(self.player,i)
        self.assertTrue(self.board.isBoardFull())
        
    # Board.isWinner()
    # Case one = top horizontal line [0,1,2]
    # X|X|X
    def testIsWinnerTrueCaseOneTrue(self):
        self.board.move(self.player,0)
        self.board.move(self.player,1)
        self.board.move(self.player,2)
        self.assertTrue(self.board.isWinner(self.player))
    
    #  | |     
    def testIsWinnerFalseCaseOneFalseBlank(self):
        self.assertFalse(self.board.isWinner(self.player))
    
    # O != X|X|X    
    def testIsWinnerFalseCaseOneWrongPlayer(self):
        self.board.move(self.player,0)
        self.board.move(self.player,1)
        self.board.move(self.player,2)
        self.assertFalse(self.board.isWinner(self.player2))
    
    # X != O|X|X
    def testIsWinnerFalseCaseOneBlocked(self):
        self.board.move(self.player2,0)
        self.board.move(self.player,1)
        self.board.move(self.player,2)
        self.assertFalse(self.board.isWinner(self.player))
        
        


if __name__ == "__main__":
    unittest.main()

