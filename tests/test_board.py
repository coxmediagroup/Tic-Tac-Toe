'''
Created on Jul 23, 2013

@author: christie
'''
import unittest
from com.cox import board

class Test(unittest.TestCase):


    def setUp(self):
        self.board = board.board(human='O', computer='X')        
    
    def test_printboard(self):        
        self.board.print_board()
    
    def test_letter_selection(self):
        self.assertTrue(self.board.players.get('human')=='O')
        self.assertTrue(self.board.players.get('computer')=='X')
        
    def test_move(self):
        self.board.move('human', '00')
        self.board.move('human', '01')
        self.board.move('human', '02')
        assert(self.board.board[0][0]=='O' and self.board.board[0][1] == 'O' and self.board.board[0][2] == 'O')
    
    def test_is_winner(self):
        player = 'human'
        self.board.move(player, '00')
        self.board.move(player, '01')
        self.board.move(player, '02')
        self.assertTrue(self.board.is_winner(player))
        self.board.board[0][2] = '-'
        self.assertFalse(self.board.is_winner(player))
    
    def test_is_board_full(self):
        for i in range(3):
            for j in range(3):
                self.board.board[i][j] = 'X'
        self.assertTrue(self.board.is_board_full())


if __name__ == "__main__":
    unittest.main()