import tictactoe


class StopGame(Exception):
    def __init__(self, winner):
        self.winner = winner


def check_winner(board):
    winner = board.get_winner()

    if winner:
        raise StopGame(board.get_winner())
        

def test_design():
    board = tictactoe.Board()
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)
    human_player = tictactoe.PLAYER_X

    try:
        board.add_move(pos=(1, 1), player=human_player)
        check_winner(board)

        board.add_move(pos=computer.get_next_move(board), player=computer.player)
        check_winner(board)
    except StopGame as e:
        print e.winner
