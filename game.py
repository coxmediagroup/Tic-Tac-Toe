#!/usr/bin/env python2.7

from board import Board
from player import KeyboardInputPlayer, AIPlayer

class TicTacToe(object):
    ''' Tic-Tac-Toe game.  Sets up the game board and pits the computer
        against a human opponent. '''
    @classmethod
    def main(cls):
        game = cls()
        game.play()


    def _game_over(self, board):
        winner = board.winner()
        if(winner is not None):
            print('%s wins!' % winner)
            return True

        draw = board.draw()
        if(draw):
            print('Game ends in a draw.')

        return draw


    def play(self):
        go = True
        while go:
            # Set up the game
            board = Board()
            player1 = AIPlayer(True, board)
            player2 = KeyboardInputPlayer(False, board)
            while True:
                # Play the game
                player1.next_move()
                if(self._game_over(board)):
                    break
                player2.next_move()
                if(self._game_over(board)):
                    break

            value = raw_input('Play again? [Y/n]: ')
            go = 'n' not in value.lower()


if __name__ == '__main__':
    TicTacToe.main()
