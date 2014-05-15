"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Game.board import (create_computer_move,
                        doesGameHaveWinner,
                        empty,
                        empty_board,
                        isGameOver,
                        Player_O,
                        Player_X,
                        validMoves,
                        validMovesLeft)

from django.test import TestCase

class boardTest(TestCase):
    def test_doesGameHaveWinner(self):
        '''
        checks to see if game has a winner
        '''
        self.assertEqual(doesGameHaveWinner(empty_board), False)

        board = [empty, empty, empty,
                 Player_X, Player_O, Player_X,
                 empty, empty, empty]
        self.assertEqual(doesGameHaveWinner(board), False)

        board = [Player_X, Player_X, Player_X,
                 empty, empty, empty,
                 empty, empty, empty]
        self.assertEqual(doesGameHaveWinner(board), True)

        board = [empty, empty, Player_O,
                 empty, Player_O, empty,
                 Player_O, empty, empty]
        self.assertEqual(doesGameHaveWinner(board), True)

        board = [empty, empty, Player_O,
                 Player_X, Player_O, Player_X,
                 Player_O, empty, empty]
        self.assertEqual(doesGameHaveWinner(board), True)



    def test_validMovesLeft(self):
        '''
        returns true or false if board has any moves left
        '''

        self.assertEqual(validMovesLeft(empty_board), True)


        board = [empty, empty, empty,
                 Player_X, Player_O, Player_X,
                 empty, empty, empty]
        self.assertEqual(validMovesLeft(board), True)


        board = [empty, Player_X, Player_O,
                 Player_X, Player_O, Player_X,
                 Player_X, Player_X, Player_O]
        self.assertEqual(validMovesLeft(board), True)


        board = [Player_X, Player_X, Player_O,
                 Player_X, Player_O, Player_X,
                 Player_X, Player_X, Player_O]
        self.assertEqual(validMovesLeft(board), False)

    def test_isGameOver(self):
        '''
        checks to see if the game is over, weather its won or no empty cells
        '''

        self.assertEqual(isGameOver(empty_board), False)

        board = [Player_X, Player_X, Player_O,
                 Player_X, Player_O, Player_X,
                 Player_X, Player_X, Player_O]
        self.assertEqual(isGameOver(board), True)

        board = [Player_X, Player_X, Player_O,
                 Player_O, Player_O, Player_X,
                 Player_X, Player_X, Player_O]
        self.assertEqual(isGameOver(board), True)

    def test_validMoves(self):
        '''
        checks the boards and returns a valid list of free cells
        '''
        self.assertEqual(validMoves(empty_board), [0, 1, 2, 3, 4, 5, 6, 7, 8] )

        board = [empty, empty, empty,
                 Player_X, Player_O, Player_X,
                 empty, empty, empty]
        self.assertEqual(validMoves(board), [0, 1, 2, 6, 7, 8] )


        board = [empty, Player_X, Player_O,
                 Player_X, Player_O, Player_X,
                 Player_X, Player_X, Player_O]
        self.assertEqual(validMoves(board), [0])


        board = [Player_X, Player_X, Player_O,
                 Player_X, Player_O, Player_X,
                 Player_X, Player_X, Player_O]
        self.assertEqual(validMoves(board), [])


    def test_create_computer_move(self):
        '''
        Tests create_computer_move algrothms 
        
        this includes frindge cases that have been experienced
        '''

        #makes sure it takes the center
        self.assertEqual(create_computer_move(empty_board), 4)


        #makes sure it will not allow user to win
        board = [empty, Player_X, Player_O,
                 Player_X, Player_O, Player_X,
                 Player_X, Player_X, Player_O]
        self.assertEqual(create_computer_move(board), 0)

        board = [Player_X, empty, empty,
                 empty, empty, empty,
                 empty, empty, empty]
        self.assertEqual(create_computer_move(board), 4)


        board = [Player_X, Player_X, empty,
                 empty, Player_O, empty,
                 empty, empty, empty]
        self.assertEqual(create_computer_move(board), 2)


        board = [Player_X, Player_X, Player_O,
                 Player_X, Player_O, empty,
                 empty, empty, empty]
        self.assertEqual(create_computer_move(board), 6)


        #to make sure it won the game
        board = [Player_X, Player_X, Player_O,
                 Player_X, Player_O, empty,
                 Player_O, empty, empty]
        self.assertEqual(create_computer_move(board), 5)


        board = [Player_X, empty, empty,
                 Player_X, Player_O, empty,
                 empty, empty, empty]
        self.assertEqual(create_computer_move(board), 6)

        board = [empty, Player_X, Player_O,
                 Player_X, Player_O, Player_X,
                 Player_X, Player_X, Player_O]
        self.assertEqual(create_computer_move(board), 0)


        board = [empty, Player_X, Player_O,
                 Player_X, Player_O, Player_X,
                 Player_X, Player_X, Player_O]
        self.assertEqual(create_computer_move(board), 0)


        board = [Player_X, Player_X, Player_O,
                 Player_X, Player_O, Player_X,
                 Player_X, Player_X, Player_O]
        self.assertEqual(create_computer_move(board), None)

        ##an issue existed in the algorthm
        board = [Player_X, Player_O, empty,
                 empty, Player_O, Player_X,
                 Player_X, empty, empty]
        self.assertEqual(create_computer_move(board), 7)


        board = [empty, Player_O, Player_X,
                 Player_O, Player_X, Player_X,
                 empty, empty, empty]
        self.assertEqual(create_computer_move(board), 6)


        board = [empty, empty, empty,
                 empty, Player_X, empty,
                 empty, empty, empty]
        self.assertEqual(create_computer_move(board), 1)
