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

        #path = response.path
        #expected = reverse('site_index')
        #self.assertEqual(path, expected, 'Expected %s but returned %s for %s'
        #% (expected, code, game_creation))

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
        self.assertContains(response, 'tic_X.png', 'Expected the CPU player to have an X on the board')


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

        #Check with a few random values
        self.gameObj.gameBoard = [['O', 'O', 'X'], ['O', 'X', ' '], [' ', 'X', ' ']]
        result = self.gameObj.checkGameOver()
        expected_return = False
        expected_winner = ' '
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))

        #Check with a horizontal win for the CPU
        self.gameObj.gameBoard = [['O', 'O', 'O'], ['O', 'X', ' X'], [' ', 'X', ' ']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = self.gameObj.cpuCharacter
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))

        #Check with a verticle win for the Player
        self.gameObj.gameBoard = [['O', 'O', 'X'], ['O', 'X', ' X'], [' ', 'O', 'X']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = self.gameObj.playerCharacter
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))

        #Check with a diagonal win for the CPU (top left to bottom right)
        self.gameObj.gameBoard = [['O', 'O', 'X'], ['X', 'O', ' X'], [' ', 'X', 'O']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = self.gameObj.cpuCharacter
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))

        #Check with a diagonal win for the player (top right to bottom left)
        self.gameObj.gameBoard = [['O', 'O', 'X'], ['O', 'X', '  '], ['X', 'X', 'O']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = self.gameObj.playerCharacter
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))

        #Check with a draw for the both players
        self.gameObj.gameBoard = [['O', 'O', 'X'], ['O', 'O', 'X '], ['X', 'X', 'O']]
        result = self.gameObj.checkGameOver()
        expected_return = True
        expected_winner = ' '
        self.assertEqual(result, expected_return, 'Expected %s but returned %s for %s'
        % (expected_return, result, 'game models checkGameOver()'))

        #TODO: Checks for some other sizes here