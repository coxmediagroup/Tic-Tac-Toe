from django.utils import unittest
from django.test.client import Client
import re
from tictactoe.tictactoe import Player, AIPlayer, Board
import simplejson

class BoardTest(unittest.TestCase):
    """
        Here go all the test cases for the tic tac toe board
    """
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.blank_board = Board(the_board=[None, None, None, None, u'X', None, None,None,None]).draw()
        self.blank_board = re.sub(r"^\s+", "", "a\n b\n c", flags = re.MULTILINE)

    def test_getInitialBoard(self):
        # Issue a GET request.
        response = self.client.get('/')
        board = Board(response.context['the_board'].the_board).draw()
        board = re.sub(r"^\s+", "", "a\n b\n c", flags = re.MULTILINE)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        #check the string returned for a default is what we expect
        self.assertEquals(board,self.blank_board)



class PlayerTest(unittest.TestCase):
    """
        Here go all the test cases for the tic tac toe AI player
    """
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        #the aiPlayer to compare against
        self.aiPlayer = AIPlayer('X')
        #the human player to compare against
        self.humanPlayer = Player('O')
        self.initial_state = [None, None, None, None, u'X', None, None, u'O', None]

    def test_MakeHumanPlayerO(self):
        # Issue a GET request.
        response = self.client.get('/?board=' + simplejson.dumps(self.initial_state))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        #check the string returned for a blank request
        self.assertEqual(response.context['human'].board_value,'O')

    def test_MakeAIPlayerX(self):
        # Issue a GET request.
        response = self.client.get('/?board=' + simplejson.dumps(self.initial_state))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        #check the string returned for a blank request
        self.assertEqual(response.context['ai'].board_value,'X')

    def test_AIMakeAMove(self):
        # Issue a GET request.
        response = self.client.get('/?board=' + simplejson.dumps(self.initial_state))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        #the initial state is contained within the returned state, very simple test to make sure a move is made
        self.assertLessEqual(self.initial_state,response.context['the_board'].the_board)

    def test_cannotWin(self):
        # Issue a GET request.

        board = Board(the_board=self.initial_state)
        # Check that the response is 200 OK.

        #check for win can win
        self.assertFalse(board.check_for_win(self.aiPlayer))

    def test_canWin(self):
        # Issue a GET request.

        board = Board(the_board=[ u'X',u'X',u'X',None, None, None, None, u'O', None])
        # Check that the response is 200 OK.
        print(board.the_board)
        #check for win win, i should be able
        self.assertTrue(board.check_for_win(self.aiPlayer))



