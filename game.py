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
        ''' Determine if the game has ended for the given board. '''
        winner = board.winner()
        if(winner is not None):
            print('%s wins!' % winner)
            return True

        draw = board.draw()
        if(draw):
            print('Game ends in a draw.')

        return draw

    def play(self):
        ''' Play the game.  Sets up the board and allows players to play until
            completion.  Continues until the user opts to quit. '''
        print('Board layout:')
        print(Board().get_layout())
        print('-' * 20)
        print('')
        go = True
        while go:
            # Set up the game
            board = Board()
            player1 = KeyboardInputPlayer(True, board)
            player2 = AIPlayer(False, board)
            players = (player1, player2)
            game_over = False
            print(str(board))
            while not game_over:
                # Play the game
                for i in range(2):
                    print('Player %d move' % (i + 1))
                    players[i].next_move()
                    print(str(board))
                    if(self._game_over(board)):
                        game_over = True
                        break

            value = raw_input('Play again? [Y/n]: ')
            go = 'n' not in value.lower()


if __name__ == '__main__':
    TicTacToe.main()
