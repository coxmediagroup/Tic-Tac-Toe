import unittest
import TicTacToeLib
from random import shuffle

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
    player=TicTacToeLib.Player(TicTacToeLib.PIECE_X)
    for i in range(numberOfMoves):
        board.move(player,i)
    return board.isBoardFull()

def checkIsWinnerVaildLine(move_list,isPlayerX=True):
    board=TicTacToeLib.Board()
    player=TicTacToeLib.Player(TicTacToeLib.PIECE_X)
    player2=TicTacToeLib.Player(TicTacToeLib.PIECE_O)
    for i in move_list:
        board.move(player,i)
    if isPlayerX:
        return board.isWinner(player)
    else:
        return board.isWinner(player2)
    
def checkIsWinnerFalse(move_list,x,o):
    board=TicTacToeLib.Board()
    player=TicTacToeLib.Player(TicTacToeLib.PIECE_X)
    player2=TicTacToeLib.Player(TicTacToeLib.PIECE_O)
    shuffle(move_list)
    
    pos = 0
    for _ in range(x):
        board.move(player, move_list[pos])
        pos+=1
    for _ in range(o):
        board.move(player2, move_list[pos])
        pos+=1
    
    return board.isWinner(player)    

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
            elif ( method_name == '_test_IsWinnerTrue' or 
                method_name == '_test_IsWinnerWrongPlayerFalse'):
                for index, item in enumerate(WIN_LIST):
                    testable_name = 'test{0}{1}'.format(testname,item[0])
                    param = True if method_name=='_test_IsWinnerTrue' else False                        
                    testable = lambda self, func=method,arg=checkIsWinnerVaildLine(item[1],param): func(self,arg)
                    testable.__name__ = testable_name
                    attrs[testable_name] = testable
                    
            elif method_name.startswith('_test_IsWinnerFalse'):
                x=o=0
                if method_name.endswith('_X1_O2'): x,o=1,2
                elif method_name.endswith('_X2_O1'): x,o=2,1
                elif method_name.endswith('_X1_O1'): x,o=1,1
                elif method_name.endswith('_X2_O0'): x,o=2,0
                elif method_name.endswith('_X0_O2'): x,o=0,2
                elif method_name.endswith('_X1_O0'): x,o=1,0
                elif method_name.endswith('_X0_O1'): x,o=0,1
                
                for index, item in enumerate(WIN_LIST):
                    testable_name = 'test{0}{1}'.format(testname,item[0])                       
                    testable = lambda self, func=method,arg=checkIsWinnerFalse(item[1],x,o): func(self,arg)
                    testable.__name__ = testable_name
                    attrs[testable_name] = testable    
                    
            

        return type.__new__(cls, name, bases, attrs)


class TicTacToeLibTests(unittest.TestCase):
    __metaclass__ = DynamicTestMaker


    def setUp(self):
        self.blanktestboard=[TicTacToeLib.BLANK]*TicTacToeLib.GAME_BOARD_SQUARE_SIZE
        self.board=TicTacToeLib.Board()
        self.player=TicTacToeLib.Player(TicTacToeLib.PIECE_X)
        self.player2=TicTacToeLib.Player(TicTacToeLib.PIECE_O)

    # Board.getGameBoard()
    def testGetGameBoard(self):
        self.assertEqual(self.blanktestboard, self.board.getGameBoard())
        
    def testGetGameBoardFalse(self):
        self.blanktestboard[0]=TicTacToeLib.PIECE_X
        self.assertNotEqual(self.blanktestboard, self.board.getGameBoard())
    
    # Board.__isValidMove    
    def testIsValidMove(self):
        # ugly but I don't need this exposed
        self.assertTrue(self.board._Board__isValidMove(0))

    def testIsValidMoveFalse(self):
        # ugly but I don't need this exposed
        self.board._Board__gameboard[0]=TicTacToeLib.PIECE_X
        # self.board.move(self.player,0)
        self.assertFalse(self.board._Board__isValidMove(0))
    
    # Board.move()     
    def testMove(self):
        self.assertTrue(self.board.move(self.player,0))
        
    def testMoveFalse(self):
        self.board._Board__gameboard[0]=TicTacToeLib.PIECE_X
        self.assertFalse(self.board.move(self.player,0))
    
    # Board.move() + Board.getGameBoard()    
    def testMoveMadeNE(self):
        self.board.move(self.player,0)
        self.assertNotEqual(self.blanktestboard, self.board.getGameBoard())
        
    def testMoveMadeEQ(self):
        self.blanktestboard[0] = TicTacToeLib.PIECE_X
        self.board.move(self.player,0)
        self.assertEqual(self.blanktestboard, self.board.getGameBoard()) 
    
    #Player.__init__()    
    def testPlayer(self):
        self.assertTrue(self.player.piece == TicTacToeLib.PIECE_X)
    
    def testPlayerFalse(self):
        self.assertFalse(self.player.piece != TicTacToeLib.PIECE_X)
        
    #Board.isBoardFull()
    def testIsBoardFullNineMoves(self):
        self.assertTrue(checkIsBoardFull(9))
    
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
    
    # blank=0/X=1/O=2
    def _test_IsWinnerFalseB0_X1_O2(self, arg):
        self.assertFalse(arg)

    # blank=0/X=2/O=1
    def _test_IsWinnerFalseB0_X2_O1(self, arg):
        self.assertFalse(arg)
        
    # blank=1/X=1/O=1
    def _test_IsWinnerFalseB1_X1_O1(self, arg):
        self.assertFalse(arg)
        
    # blank=1/X=2/O=0
    def _test_IsWinnerFalseB1_X2_O0(self, arg):
        self.assertFalse(arg)
        
    # blank=1/X=0/O=2
    def _test_IsWinnerFalseB1_X0_O2(self, arg):
        self.assertFalse(arg)
        
    # blank=2/X=1/O=0
    def _test_IsWinnerFalseB2_X1_O0(self, arg):
        self.assertFalse(arg)
        
    # blank=2/X=0/O=1
    def _test_IsWinnerFalseB2_X0_O1(self, arg):
        self.assertFalse(arg)
        
    # AIPlayer().__init__()
    def testAIPlayer(self):
        self.aiPlayer = TicTacToeLib.AIPlayer(TicTacToeLib.PIECE_O)
        self.assertTrue(self.aiplayer.piece == TicTacToeLib.PIECE_O)
    
    def testAIPlayerFalse(self):
        self.aiPlayer = TicTacToeLib.AIPlayer(TicTacToeLib.PIECE_O)
        self.assertFalse(self.aiplayer.piece != TicTacToeLib.PIECE_O)
    
    

if __name__ == "__main__":
    unittest.main()

