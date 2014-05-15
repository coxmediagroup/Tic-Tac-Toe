from board_evaluator import detect_win

def play_game(player_one_algorithm, player_two_algorithm):
    player_one = Player()
    player_one.move_function = player_one_algorithm
    player_one.number = 1
    player_two = Player()
    player_two.move_function = player_two_algorithm
    player_two.number = 2
    player_iter = iter([
        player_one,
        player_two,
        player_one,
        player_two,
        player_one,
        player_two,
        player_one,
        player_two,
        player_one,
    ])
    board = [[0,0,0],[0,0,0],[0,0,0]]
    for player in player_iter:
        row, column = player.make_move(board)
        board[row][column] = player.number
        winner = detect_win(board)
        if winner:
            print 'player ' + str(winner) + ' wins.'
            break
    else:
        print 'cat game. nobody wins.'

class Player(object):
    '''number: the number of this player.
move_function: the function that actually makes moves'''
    def make_move(self, board):
        return self.move_function(board, self.number)
