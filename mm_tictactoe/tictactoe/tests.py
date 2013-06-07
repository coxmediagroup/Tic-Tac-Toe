"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from models import Player, Game

class TicTacToeTest(TestCase):
    def __playGame(self):
        player1 = Player(name="player1")
        player2 = Player(name="player2")
        game = Game(player1=player1, player2=player2)
        game.nextTurn(Game.X)
        game.nextTurn(Game.O)
        game.nextTurn(Game.X)
        game.nextTurn(Game.O)
        game.nextTurn(Game.X)
        game.nextTurn(Game.O)
        game.nextTurn(Game.X)
        game.nextTurn(Game.O)
        game.nextTurn(Game.X)
        return game

    def test_3GamesToDraw(self):
        """
        Simply play three games with computer X and O moves, and make
        sure nobody wins.
        """
        game1 = self.__playGame()
        self.assertEqual(filter(lambda x: x==0, game1.board), [])
        self.assertFalse(game1.checkWinner(game1.X))
        self.assertFalse(game1.checkWinner(game1.O))

        game2 = self.__playGame()
        self.assertEqual(filter(lambda x: x==0, game2.board), [])
        self.assertFalse(game2.checkWinner(game2.X))
        self.assertFalse(game2.checkWinner(game2.O))

        game3 = self.__playGame()
        self.assertEqual(filter(lambda x: x==0, game3.board), [])
        self.assertFalse(game3.checkWinner(game3.X))
        self.assertFalse(game3.checkWinner(game3.O))


    def test_winBeforeBlock(self):
        """
        The computer move should win the game before blocking.  Also,
        the nextTurn() method should return True, since this move produced
        a winner, and the checkWin() method should return true for X, but
        false for O.

        Starting board:
            O O _
            X X _
            _ _ _

            It's the X player's turn.  It should win the game as such:
            O O _
            X X X
            _ _ _

        """

        startingBoard = [Game.O, Game.O, Game.EMPTY,
                    Game.X, Game.X, Game.EMPTY,
                    Game.EMPTY, Game.EMPTY, Game.EMPTY]


        expected = [Game.O, Game.O, Game.EMPTY,
                    Game.X, Game.X, Game.X,
                    Game.EMPTY, Game.EMPTY, Game.EMPTY]

        player1 = Player(name="player1")
        player2 = Player(name="player2")
        game = Game(player1=player1, player2=player2)
        game.board = startingBoard
        game.turn = 4
        win = game.nextTurn(Game.X)
        self.assertEqual(game.board, expected)
        self.assertTrue(win)
        self.assertTrue(game.checkWinner(game.X))
        self.assertFalse(game.checkWinner(game.O))

    def test_blockWin(self):
        """
        Block a potential win before a fork.  Starting board:
            O _ X
            _ X _
            O _ _

        The computer should block the potential win by putting an X
        between the two O's.  There is a potential fork by placing an X
        in the empty spot to the right of the X, but that would mean the
        O's could win.
        """

        startingBoard = [Game.O, Game.EMPTY, Game.X,
                    Game.EMPTY, Game.X, Game.EMPTY,
                    Game.O, Game.EMPTY, Game.EMPTY]


        expected = [Game.O, Game.EMPTY, Game.X,
                Game.X, Game.X, Game.EMPTY,
                Game.O, Game.EMPTY, Game.EMPTY]

        player1 = Player(name="player1")
        player2 = Player(name="player2")
        game = Game(player1=player1, player2=player2)
        game.board = startingBoard
        game.turn = 4
        game.nextTurn(Game.X)
        self.assertEqual(game.board, expected)


