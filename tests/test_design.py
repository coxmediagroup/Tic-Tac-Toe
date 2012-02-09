"""
import tictactoe


class StopGame(Exception):
    pass


def check_winner(board):
    if board.has_winner():
        raise StopGame(board.get_winner())
        

def test_design():
    board = tictactoe.Board()
    computer = tictactoe.AIPlayer(circle=True)
    human_player = 'cross'

    try:
        board.add_move(pos=(1, 1), player=human_player)

        computejj


        



"""
