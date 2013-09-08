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
    for i in xrange(numberOfMoves):
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
    for _ in xrange(x):
        board.move(player, move_list[pos])
        pos+=1
    for _ in xrange(o):
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
        self.aiplayer=TicTacToeLib.AIPlayer(TicTacToeLib.PIECE_O)
        self.aiplayer2=TicTacToeLib.AIPlayer(TicTacToeLib.PIECE_X)

    # Board.getGameBoard()
    def testGetGameBoard(self):
        self.assertEqual(self.blanktestboard, self.board.getGameBoard())
        
    def testGetGameBoardFalse(self):
        self.blanktestboard[0]=TicTacToeLib.PIECE_X
        self.assertNotEqual(self.blanktestboard, self.board.getGameBoard())
    
    # Board.isValidMove    
    def testIsValidMove(self):
        self.assertTrue(self.board.isValidMove(TicTacToeLib.UPPER_LEFT_CORNER))

    def testIsValidMoveFalse(self):
        # ugly but I don't need this exposed
        self.board._Board__gameboard[TicTacToeLib.UPPER_LEFT_CORNER]=TicTacToeLib.PIECE_X
        # self.board.move(self.player,0)
        self.assertFalse(self.board.isValidMove(TicTacToeLib.UPPER_LEFT_CORNER))
    
    # Board.move()     
    def testMove(self):
        self.assertTrue(self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER))
        
    def testMoveFalse(self):
        self.board._Board__gameboard[TicTacToeLib.UPPER_LEFT_CORNER]=TicTacToeLib.PIECE_X
        self.assertFalse(self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER))
    
    # Board.move() + Board.getGameBoard()    
    def testMoveMadeNE(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.assertNotEqual(self.blanktestboard, self.board.getGameBoard())
        
    def testMoveMadeEQ(self):
        self.blanktestboard[0] = TicTacToeLib.PIECE_X
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
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
    def testAIPlayerEQ(self):
        self.assertEqual(self.aiplayer.piece, TicTacToeLib.PIECE_O)
    
    def testAIPlayerNE(self):
        self.assertNotEqual(self.aiplayer.piece, TicTacToeLib.PIECE_X)
            
    # AIPlayer.__hasMadeInitialMove will be True after AI Player's first move
    def testAIPlayerHasMadeInitialMoveF(self):
        self.assertFalse(self.aiplayer._AIPlayer__hasMadeInitialMove)
        
    def testAIPlayerHasMadeInitialMoveT(self):
        self.aiplayer.move(self.board)
        self.assertTrue(self.aiplayer._AIPlayer__hasMadeInitialMove)
    
    # Board.getTotalMovesMade    
    def testBoardGetTotalMovesMadeEQZero(self):
        self.assertEqual(0,self.board.getTotalMovesMade())
        
    def testBoardGetTotalMovesMadeEQOne(self):
        self.board.move(self.player, TicTacToeLib.UPPER_LEFT_CORNER)
        self.assertEqual(1,self.board.getTotalMovesMade())
        
    def testBoardGetTotalMovesMadeEQTwo(self):
        self.board.move(self.player, TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player, TicTacToeLib.UPPER_EDGE)
        self.assertEqual(2,self.board.getTotalMovesMade())

    
    def testBoardGetTotalMovesMadeNEZero(self):
        self.board.move(self.player, TicTacToeLib.UPPER_LEFT_CORNER)
        self.assertNotEqual(0,self.board.getTotalMovesMade())
        
    def testBoardGetTotalMovesMadeNEOne(self):
        self.assertNotEqual(1,self.board.getTotalMovesMade())
        
    def testBoardGetTotalMovesMadeNETwo(self):
        self.board.move(self.player, TicTacToeLib.UPPER_LEFT_CORNER)
        self.assertNotEqual(2,self.board.getTotalMovesMade())

    #AIPlayer.__initialMove(board)   
    def testAIPlayerInitialMoveOffense(self):
        self.assertEqual(TicTacToeLib.UPPER_LEFT_CORNER,self.aiplayer._AIPlayer__initialMove(self.board))
        
    def testAIPlayerInitialMoveDefenseHumanPlaysNonCenter(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.assertEqual(TicTacToeLib.CENTER,self.aiplayer._AIPlayer__initialMove(self.board))
        
    def testAIPlayerInitialMoveDefenseHumanPlaysCenter(self):
        self.board.move(self.player,TicTacToeLib.CENTER)
        self.assertEqual(TicTacToeLib.UPPER_LEFT_CORNER,self.aiplayer._AIPlayer__initialMove(self.board))
        
    def testAIPlayerInitialMoveInvalid(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player,TicTacToeLib.CENTER)
        self.assertEqual(TicTacToeLib.INVALID_MOVE, self.aiplayer._AIPlayer__initialMove(self.board))

        
    #AIPlayer.moveAI(board)   
    def testAIPlayerMoveFirstMoveOffense(self):
        self.assertEqual(TicTacToeLib.UPPER_LEFT_CORNER,self.aiplayer.move(self.board))
        
    def testAIPlayerMoveFirstMoveDefenseHumanPlaysNonCenter(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.assertEqual(TicTacToeLib.CENTER,self.aiplayer.move(self.board))
        
    def testAIPlayerMoveFirstMoveDefenseHumanPlaysCenter(self):
        self.board.move(self.player,TicTacToeLib.CENTER)
        self.assertEqual(TicTacToeLib.UPPER_LEFT_CORNER,self.aiplayer.move(self.board))
    
    def testAIPlayerMoveFirstMoveInvalid(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player,TicTacToeLib.CENTER)
        self.assertEqual(TicTacToeLib.INVALID_MOVE, self.aiplayer.move(self.board))

    #AIPlayer.__opponentPiece()
    def testAIPlayerOpponentPieceOTrue(self):
        self.assertEqual(TicTacToeLib.PIECE_O,self.aiplayer2._AIPlayer__opponentPiece())

    def testAIPlayerOpponentPieceOFalse(self):
        self.assertNotEqual(TicTacToeLib.PIECE_O,self.aiplayer._AIPlayer__opponentPiece())

    def testAIPlayerOpponentPieceXTrue(self):
        self.assertEqual(TicTacToeLib.PIECE_X,self.aiplayer._AIPlayer__opponentPiece())

    def testAIPlayerOpponentPieceXFalse(self):
        self.assertNotEqual(TicTacToeLib.PIECE_X,self.aiplayer2._AIPlayer__opponentPiece())
    
    #Board.findFirstWinningMove(piece) X| |X vs X
    def testfindFirstWinningMoveTrue(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.assertEqual(TicTacToeLib.UPPER_EDGE, self.aiplayer2._AIPlayer__findFirstWinningMove(self.board, self.aiplayer2))
    
    #Board.findFirstWinningMove(piece) O| |O vs X    
    def testfindFirstWinningMoveNone(self):
        self.board.move(self.player2,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player2,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.assertEqual(TicTacToeLib.NO_MOVE, self.aiplayer2._AIPlayer__findFirstWinningMove(self.board, self.aiplayer2))
    
    def testfindFirstWinningMoveEmptyBoard(self):
        self.assertEqual(TicTacToeLib.NO_MOVE, self.aiplayer2._AIPlayer__findFirstWinningMove(self.board, self.aiplayer2))
    
    def testfindFirstWinningMoveFullBoard(self):
        for i in xrange(TicTacToeLib.GAME_BOARD_SQUARE_SIZE):
            self.board.move(self.player, i)
        self.assertEqual(TicTacToeLib.NO_MOVE, self.aiplayer2._AIPlayer__findFirstWinningMove(self.board, self.aiplayer2))
    
    #AIPlayer.__checkForWin O| |O vs O
    def testCheckForWinTrue(self):
        self.board.move(self.player2,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player2,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.assertEqual(TicTacToeLib.UPPER_EDGE, self.aiplayer._AIPlayer__checkForWin(self.board))
    
    #AIPlayer.__checkForWin O| |O vs X    
    def testCheckForWinNone(self): 
        self.board.move(self.player2,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player2,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.assertEqual(TicTacToeLib.NO_MOVE, self.aiplayer2._AIPlayer__checkForWin(self.board))

    #AIPlayer.__checkForBlock X| |X vs. O
    def testCheckForBlockTrue(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.assertEqual(TicTacToeLib.UPPER_EDGE, self.aiplayer._AIPlayer__checkForBlock(self.board))
    
    #AIPlayer.__checkForBlock X| |X vs. X    
    def testCheckForBlockNone(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.assertEqual(TicTacToeLib.NO_MOVE, self.aiplayer2._AIPlayer__checkForBlock(self.board))

    #AIPlayer.__findFork
    # X|O|X
    #  | | 
    # O| | 
    # if X next move fork at lower right corner
    # if O next move fork at lower edge

    def testFindForkTrue1(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player2,TicTacToeLib.UPPER_EDGE)
        self.board.move(self.player,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.board.move(self.player2,TicTacToeLib.LOWER_LEFT_CORNER)
        self.assertEqual(TicTacToeLib.LOWER_RIGHT_CORNER, self.aiplayer2._AIPlayer__findFork(self.board,self.aiplayer2))
        
    def testFindForkTrue2(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player2,TicTacToeLib.UPPER_EDGE)
        self.board.move(self.player,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.board.move(self.player2,TicTacToeLib.LOWER_LEFT_CORNER)
        self.assertEqual(TicTacToeLib.LOWER_EDGE, self.aiplayer._AIPlayer__findFork(self.board,self.aiplayer))
    
    # X|O|X
    #  | |
    # O|X| 
    # O should have no fork
    def testFindForkNoMove(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player2,TicTacToeLib.UPPER_EDGE)
        self.board.move(self.player,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.board.move(self.player2,TicTacToeLib.LOWER_LEFT_CORNER)
        self.board.move(self.player,TicTacToeLib.LOWER_EDGE)
        self.assertEqual(TicTacToeLib.NO_MOVE, self.aiplayer._AIPlayer__findFork(self.board,self.aiplayer))
    
    # same board setup and results expected as __findFork
    def testCheckForForkTrue1(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player2,TicTacToeLib.UPPER_EDGE)
        self.board.move(self.player,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.board.move(self.player2,TicTacToeLib.LOWER_LEFT_CORNER)
        self.assertEqual(TicTacToeLib.LOWER_RIGHT_CORNER, self.aiplayer2._AIPlayer__checkForFork(self.board))
        
    def testCheckForForkTrue2(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player2,TicTacToeLib.UPPER_EDGE)
        self.board.move(self.player,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.board.move(self.player2,TicTacToeLib.LOWER_LEFT_CORNER)
        self.assertEqual(TicTacToeLib.LOWER_EDGE, self.aiplayer._AIPlayer__checkForFork(self.board))
    
    # X|O|X
    #  | |
    # O|X| 
    # O should have no fork
    def testCheckForForkNoMove(self):
        self.board.move(self.player,TicTacToeLib.UPPER_LEFT_CORNER)
        self.board.move(self.player2,TicTacToeLib.UPPER_EDGE)
        self.board.move(self.player,TicTacToeLib.UPPER_RIGHT_CORNER)
        self.board.move(self.player2,TicTacToeLib.LOWER_LEFT_CORNER)
        self.board.move(self.player,TicTacToeLib.LOWER_EDGE)
        self.assertEqual(TicTacToeLib.NO_MOVE, self.aiplayer._AIPlayer__checkForFork(self.board))
    
    # TODO tests for getFork() getOpponentFork() ? 

    # Board.validMoveList()
    # check zero moves, nine moves, one move
    def testValidMoveListZeroMoves(self):
        testlist = [0,1,2,3,4,5,6,7,8]
        self.assertEqual(testlist,self.board.validMoveList())
        
    def testValidMoveListNineMoves(self):
        testlist = []
        for i in xrange(TicTacToeLib.GAME_BOARD_SQUARE_SIZE):
            self.board.move(self.player,i)
        self.assertEqual(testlist,self.board.validMoveList())

    def testValidMoveListOneMoveCenter(self):
        testlist = [0,1,2,3,5,6,7,8]
        self.board.move(self.player,TicTacToeLib.CENTER)
        self.assertEqual(testlist,self.board.validMoveList())
        

    

if __name__ == "__main__":
    unittest.main()

