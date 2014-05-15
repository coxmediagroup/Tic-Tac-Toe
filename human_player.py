from game_constants import player_symbol_converter,\
     coordinate_representation_reverse_map

def make_move(board, player_number):
    print board_tostring(board)
    return ask_user_for_move(player_number)

def board_tostring(board):
    player_symbol_converter
    result = list()
    result.append(' 123\n')
    row_label_iter = iter('abc')
    for row in board:
        result.append(next(row_label_iter))
        #result.append(' ')
        for element in row:
            result.append(player_symbol_converter[element])
        result.append('\n')
    return ''.join(result)

def ask_user_for_move(player_number):
    print player_symbol_converter[player_number] + "'s turn"
    i = raw_input('rc - row is a letter. column is a number. (a1, b3, c2): ')
    return coordinate_representation_reverse_map[i]
