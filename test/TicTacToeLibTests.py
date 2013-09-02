import unittest
import TicTacToeLib

NUMBER_LIST = ['EmptyBoard', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']
WIN_LIST =  [
             ['HorizontalUpper',    [0,1,2] ],
             ['HorizontalMiddle',   [3,4,5] ], 
             ['HorizontalLower',    [6,7,8] ],
             ['VerticalLeft',       [0,3,6] ],
             ['VerticalCenter',     [1,4,7] ],
             ['VerticalRight',      [2,5,8] ],
             ['DiagonalLeft',       [0,4,8] ],
             ['DiagonalRight',      [2,4,6] ]
            ]

def checkIsBoardFull(numberOfMoves):
    board=TicTacToeLib.Board()
    player=TicTacToeLib.Player('X')
    for i in range(numberOfMoves):
        board.move(player,i)
    return board.isBoardFull()

def checkIsWinnerVaildLine(move_list,isPlayerX=True):
    board=TicTacToeLib.Board()
    player=TicTacToeLib.Player('X')
    player2=TicTacToeLib.Player('O')
    for i in move_list:
        board.move(player,i)
    if isPlayerX:
        return board.isWinner(player)
    else:
        return board.isWinner(player2)

# any tests built with this class will have a test_ prefix
class DynamicTestMaker(type):

    def __new__(cls, name, bases, attrs):
        callables = dict([
            (method_name, method) for (method_name, method) in attrs.items() if
            method_name.startswith('_test')
        ])

        for method_name, method in callables.items():
            assert callable(method)
            _, _, testname = method_name.partition('_test')
            
            if method_name == '_test_IsBoardFull':
                for index, item in enumerate(NUMBER_LIST):
                    testable_name = 'test{0}{1}'.format(testname,item)
                    if index > 0:
                        testable_name = 'test{0}{1}Moves'.format(testname,item)                        
                    testable = lambda self, func=method,arg=checkIsBoardFull(index): func(self,arg)
                    testable.__name__ = testable_name
                    attrs[testable_name] = testable
            if ( method_name == '_test_IsWinnerTrue' or 
                method_name == '_test_IsWinnerWrongPlayerFalse'):
                for index, item in enumerate(WIN_LIST):
                    testable_name = 'test{0}{1}'.format(testname,item[0])
                    param = True if method_name=='_test_IsWinnerTrue' else False                        
                    testable = lambda self, func=method,arg=checkIsWinnerVaildLine(item[1],param): func(self,arg)
                    testable.__name__ = testable_name
                    attrs[testable_name] = testable

        return type.__new__(cls, name, bases, attrs)


class TicTacToeLibTests(unittest.TestCase):
    __metaclass__ = DynamicTestMaker


    def setUp(self):
        self.blanktestboard=[TicTacToeLib.BLANK]*TicTacToeLib.GAME_BOARD_SQUARE_SIZE
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
    def testIsBoardFullNineMoves(self):
        for i in range(9):
            self.board.move(self.player,i)
        self.assertTrue(self.board.isBoardFull())
    
    def _test_IsBoardFull(self, arg):
        self.assertFalse(arg)
        
    # Board.isWinner()
    #  | |     
    def testIsWinnerBlankFalse(self):
        self.assertFalse(self.board.isWinner(self.player))
    
    # Case one = top horizontal line [0,1,2]
    # X == X|X|X
    def _test_IsWinnerTrue(self,arg):
        self.assertTrue(arg)

    # O != X|X|X
    def _test_IsWinnerWrongPlayerFalse(self, arg):
        self.assertFalse(arg)
        
    # X != X| |O
    def testIsWinnerOneBlankOnePieceFalse(self):
        self.board.move(self.player,0)
        self.board.move(self.player,2)
        self.assertFalse(self.board.isWinner(self.player))
        
    # X != O|X|X
    def testIsWinnerFalseCaseOneTwoPieces(self):
        self.board.move(self.player2,0)
        self.board.move(self.player,1)
        self.board.move(self.player,2)
        self.assertFalse(self.board.isWinner(self.player))
        
    # X != O|X|O
    def testIsWinnerFalseCaseOneSinglePiece(self):
        self.board.move(self.player2,0)
        self.board.move(self.player,1)
        self.board.move(self.player2,2)
        self.assertFalse(self.board.isWinner(self.player))
        
        


if __name__ == "__main__":
    unittest.main()

