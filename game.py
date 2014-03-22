from random import choice
from copy import deepcopy


CLEAN_BOARD = [
    ['', '', ''],
    ['', '', ''],
    ['', '', ''],
]


def _is_corner(cell):
    return cell in ['cell-0:0', 'cell-0:2', 'cell-2:0', 'cell-2:2']


def _is_edge(cell):
    return cell in ['cell-0:1', 'cell-1:0', 'cell-1:2', 'cell-2:1']


def ai_move_one():
    choices = ['cell-0:0', 'cell-0:2', 'cell-1:1', 'cell-2:0', 'cell-2:2']
    return choice(choices)


def calc_ai_move(player_cells, ai_cells):
    ai_first = len(ai_cells) + 1 > len(player_cells)
    turn = len(player_cells) + len(ai_cells) + 1

    board = deepcopy(CLEAN_BOARD)
    for cell in player_cells:
        row, col = cell.replace('cell-', '').split(':')
        board[int(row)][int(col)] = 'P'
    for cell in ai_cells:
        row, col = cell.replace('cell-', '').split(':')
        board[int(row)][int(col)] = 'AI'

    if turn == 3:
        if ai_first and _is_corner(ai_cells[0]):
            for row in range(3):
                for col in range(3):
                    work_board = deepcopy(board)
                    chosen_cell = 'cell-{}:{}'.format(row, col)
                    if work_board[row][col] != '':
                        continue
                    elif _is_edge(chosen_cell):
                        continue

                    work_board[row][col] = 'AI'

                    if work_board[0].count('AI') == 2 and 'P' not in work_board[0]:
                        return chosen_cell
                    elif work_board[2].count('AI') == 2 and 'P' not in work_board[2]:
                        return chosen_cell

                    col_row = (work_board[0][0], work_board[1][0], work_board[2][0])
                    if col_row.count('AI') == 2 and 'P' not in col_row:
                        return chosen_cell

                    col_row = (work_board[0][2], work_board[1][2], work_board[2][2])
                    if col_row.count('AI') == 2 and 'P' not in col_row:
                        return chosen_cell

    raise NotImplementedError
