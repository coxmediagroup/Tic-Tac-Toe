import logging

from django.test import TestCase
from django.http import HttpRequest
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client

from tictactoe.game.models import TicTacToeModel


class GameViewsTest(TestCase):
    def test_index(self):
        """
        Test the index view of the application.
        """
        game_index = reverse('site-index')

        response = self.client.get(game_index)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_index))

    def test_createGame(self):
        """
        Test the creation of the game board.
        """
        game_creation = reverse('game:createGame')

        #Get request should redirect.
        response = self.client.get(game_creation)
        code = response.status_code
        expected = 303
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))

        #Test with fully invalid form
        form_data = {'blah': 'blah',
                     'size': 3,}
        response = self.client.post(game_creation, data=form_data)
        code = response.status_code
        expected = 303
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))

        #Test with valid params but invalid range input
        form_data = {'boardSize': 10,
                     'playerCharacter': 'C',}
        response = self.client.post(game_creation, data=form_data)
        code = response.status_code
        expected = 303
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))

        #Test with valid params but non-integer value for size
        form_data = {'boardSize': 'y',
                     'playerCharacter': 'X',}
        response = self.client.post(game_creation, data=form_data)
        code = response.status_code
        expected = 303
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))


        #Test with correct form of 3 with player 1
        form_data = {'boardSize': '3',
                     'playerCharacter': 'X',}
        response = self.client.post(game_creation, data=form_data)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))

        #Test with correct form of 4 with player 2
        form_data = {'boardSize': '4',
                     'playerCharacter': 'O',}
        response = self.client.post(game_creation, data=form_data)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))
        self.assertContains(response, 'tic_X.png', msg_prefix='Expected the CPU player to have an X on the board')


class GameModelsTest(TestCase):
    def setUp(self):
        self.gameObj = TicTacToeModel.objects.create(
            boardSize = 3,
            gameBoard = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
            playerCharacter = 'X',
            cpuCharacter = 'O',
            sessionID = 'testing'
        )

    def test_checkGameOver(self):
        #Check with its blank state
        result = self.gameObj.checkGameOver()
        expected_return = False
        expected_winner = ' '
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
            % (expected_return, result, 'game models checkGameOver()'))
        self.assertEqual(self.gameObj.winner, expected_winner, 'Expected %s but returned %s for %s'
            % (expected_winner, self.gameObj.winner, 'game models checkGameOver() winner'))

        #Check with a few random values
        self.gameObj.gameBoard = [['O', 'O', 'X'], ['O', 'X', ' '], [' ', 'X', ' ']]
        result = self.gameObj.checkGameOver()
        expected_return = False
        expected_winner = ' '
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))
        self.assertEqual(self.gameObj.winner, expected_winner, 'Expected %s but returned %s for %s'
        % (expected_winner, self.gameObj.winner, 'game models checkGameOver() winner'))

        #Check with a horizontal win for the CPU
        self.gameObj.gameBoard = [['O', 'O', 'O'], ['O', 'X', ' X'], [' ', 'X', ' ']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = self.gameObj.cpuCharacter
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))
        self.assertEqual(self.gameObj.winner, expected_winner, 'Expected %s but returned %s for %s'
        % (expected_winner, self.gameObj.winner, 'game models checkGameOver() winner'))

        #Check with a verticle win for the Player
        self.gameObj.gameBoard = [['O', 'O', 'X'], ['O', 'X', ' X'], [' ', 'O', 'X']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = self.gameObj.playerCharacter
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))
        self.assertEqual(self.gameObj.winner, expected_winner, 'Expected %s but returned %s for %s'
        % (expected_winner, self.gameObj.winner, 'game models checkGameOver() winner'))

        #Check with a diagonal win for the CPU (top left to bottom right)
        self.gameObj.gameBoard = [['O', 'O', 'X'], ['X', 'O', ' X'], [' ', 'X', 'O']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = self.gameObj.cpuCharacter
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))
        self.assertEqual(self.gameObj.winner, expected_winner, 'Expected %s but returned %s for %s'
        % (expected_winner, self.gameObj.winner, 'game models checkGameOver() winner'))

        #Check with a diagonal win for the player (top right to bottom left)
        self.gameObj.gameBoard = [['O', 'O', 'X'], ['O', 'X', '  '], ['X', 'X', 'O']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = self.gameObj.playerCharacter
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))
        self.assertEqual(self.gameObj.winner, expected_winner, 'Expected %s but returned %s for %s'
        % (expected_winner, self.gameObj.winner, 'game models checkGameOver() winner'))

        #Check with a draw for the both players
        self.gameObj.gameBoard = [['X', 'O', 'X'], ['O', 'X', 'X '], ['O', 'X', 'O']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = ' '
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))
        self.assertEqual(self.gameObj.winner, expected_winner, 'Expected %s but returned %s for %s'
        % (expected_winner, self.gameObj.winner, 'game models checkGameOver() winner'))

        #Change the characters and game board size
        self.gameObj = TicTacToeModel.objects.create(
            boardSize = 4,
            gameBoard = [[' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']],
            playerCharacter = 'O',
            cpuCharacter = 'X',
            sessionID = 'testing'
        )

        #Check with a draw for the both players on 4 sizes
        self.gameObj.gameBoard = [['X', 'O', 'X', 'O'], ['O', 'O', 'X', 'O'], ['X', 'X', 'O', 'X'], ['X', 'O', 'O', 'X']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = ' '
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))
        self.assertEqual(self.gameObj.winner, expected_winner, 'Expected %s but returned %s for %s'
        % (expected_winner, self.gameObj.winner, 'game models checkGameOver() winner'))

        #Check with a horizontal win for the CPU
        self.gameObj.gameBoard = [['O', 'O', 'X', 'X'], ['O', 'O', 'X ', 'O'], ['X', 'X', 'X', 'X'], ['X', 'O', 'O', 'O']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = self.gameObj.cpuCharacter
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))
        self.assertEqual(self.gameObj.winner, expected_winner, 'Expected %s but returned %s for %s'
        % (expected_winner, self.gameObj.winner, 'game models checkGameOver() winner'))

        #Check with a vertical win for the Player
        self.gameObj.gameBoard = [['O', ' ', 'X', ' '], ['O', 'O', '  ', ' '], ['O', 'X', 'X', 'X'], ['O', 'X', ' ', ' ']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = self.gameObj.playerCharacter
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))
        self.assertEqual(self.gameObj.winner, expected_winner, 'Expected %s but returned %s for %s'
        % (expected_winner, self.gameObj.winner, 'game models checkGameOver() winner'))

        #TODO: Checks for some other sizes and variations

    def test_calculateCPUMove(self):

        #Test for a block of X winning
        self.gameObj.gameBoard = [[' ', ' ', ' '], ['O', ' ', '  '], [' ', 'X', 'X']]
        self.gameObj.calculateCPUMove()
        self.assertEqual(self.gameObj.gameBoard[2][0], 'O', 'Expected CPU move to block X winning')

        #Test that it will pick winning
        self.gameObj.gameBoard = [[' ', 'X', ' '], ['O', 'O', ' '], [' ', 'X', 'X']]
        self.gameObj.calculateCPUMove()
        self.assertEqual(self.gameObj.gameBoard[1][2], 'O', 'Expected CPU to pick winning')

        #Test that it will pick stop a corner play by going for 3 in a row
        self.gameObj.gameBoard = [['X', 'O', ' '], [' ', ' ', ' O'], [' ', ' ', 'X']]
        self.gameObj.calculateCPUMove()
        self.assertEqual(self.gameObj.gameBoard[1][1], 'O', 'Expected CPU to stop corner play and go for 3 in a row')

        #TODO: More AI checks using theories from: http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy

