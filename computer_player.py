from random import choice
from board_evaluator import detect_win

def make_move(board, player_number):
    decisions = scenario_map[board_hash(board)]
    win_decision = decisions[player_number]
    if win_decision:
        return choice(win_decision)
    cat_decision = decisions[0]
    if cat_decision:
        return choice(cat_decision)
    lose_decision = decisions[3 - player_number]
    if lose_decision:
        return choice(lose_decision)
    raise Exception('there are no legal moves to make')

def board_hash(board):
    result = 0
    for row in board:
        for element in row:
            result = result * 3 + element
    return result

scenario_map = dict()

def build_scenario_map(board, turn_number, player_number):
    hashed_board = board_hash(board)
    if hashed_board in scenario_map:
        return scenario_map[hashed_board][3]
    else:
        winning_player = detect_win(board)
        if winning_player:
            # somebody won
            scenario_map[hashed_board] = ([], [], [], winning_player)
            return winning_player
        else:
            if 9 == turn_number:
                #obvious tie game
                scenario_map[hashed_board] = ([], [], [], 0)
                return 0
            else:
                #something will happen in the future
                decisions = loopyblar(board, turn_number, player_number)
                scenario_map[hashed_board] = decisions
                return decisions[3]

def loopyblar(board, turn_number, player_number):
    decisions = [list(), list(), list(), None]
    for y in range(3):
        for x in range(3):
            if 0 == board[y][x]:
                board[y][x] = player_number
                winner = build_scenario_map(board, turn_number + 1, 3 - player_number)
                board[y][x] = 0
                decisions[winner].append((y,x))
    if decisions[player_number]:
        decisions[3] = player_number
    elif decisions[0]:
        decisions[3] = 0
    elif decisions[3 - player_number]:
        decisions[3] = 3 - player_number
    else:
        raise Exception('there are no legal moves to make')
    return decisions

build_scenario_map([[0,0,0],[0,0,0],[0,0,0]], 0, 1)
