import logging
logging.basicConfig(level=logging.DEBUG)
from random import choice
from copy import deepcopy


CLEAN_BOARD = [
    ['', '', ''],
    ['', '', ''],
    ['', '', ''],
]

AI = 'AI'
P = 'P'


def _is_corner(cell):
    return cell in ['cell-0:0', 'cell-0:2', 'cell-2:0', 'cell-2:2']


def _is_edge(cell):
    return cell in ['cell-0:1', 'cell-1:0', 'cell-1:2', 'cell-2:1']


def ai_move_one():
    choices = ['cell-0:0', 'cell-0:2', 'cell-1:1', 'cell-2:0', 'cell-2:2']
    return choice(choices)


def calc_ai_move(player_cells, ai_cells):
    ai_first = len(ai_cells) + 1 > len(player_cells)
    logging.debug('ai_first: %s', ai_first)
    turn = len(player_cells) + len(ai_cells) + 1
    logging.debug('turn: %s', turn)

    board = deepcopy(CLEAN_BOARD)
    for cell in player_cells:
        row, col = cell.replace('cell-', '').split(':')
        board[int(row)][int(col)] = P
    for cell in ai_cells:
        row, col = cell.replace('cell-', '').split(':')
        board[int(row)][int(col)] = AI

    if turn == 3:
        if ai_first and _is_corner(ai_cells[0]):
            logging.debug('ai started in corner cell')
            for row in range(3):
                for col in range(3):
                    work_board = deepcopy(board)
                    chosen_cell = 'cell-{}:{}'.format(row, col)
                    if work_board[row][col] != '':
                        logging.debug('%s is occupied, moving on', chosen_cell)
                        continue
                    elif _is_edge(chosen_cell):
                        logging.debug('%s is an edge cell, moving on', chosen_cell)
                        continue

                    work_board[row][col] = AI

                    col_row1 = (work_board[0][0], work_board[1][0], work_board[2][0])
                    col_row2 = (work_board[0][2], work_board[1][2], work_board[2][2])
                    if (work_board[0].count(AI) == 2 and P not in work_board[0]
                            or work_board[2].count(AI) == 2 and P not in work_board[2]
                            or col_row1.count(AI) == 2 and P not in col_row1
                            or col_row2.count(AI) == 2 and P not in col_row2):
                        logging.debug('next ai move: %s', chosen_cell)
                        return chosen_cell

    elif turn == 5:
        if ai_first and _is_corner(ai_cells[0]):
            logging.debug('ai started in corner cell')
            logging.debug('checking for block attempt')
            # check for a block attempt
            block_attempt = False
            col_row1 = (board[0][0], board[1][0], board[2][0])
            col_row2 = (board[0][2], board[1][2], board[2][2])
            if (board[0].count(AI) == 2 and P in board[0]
                    or board[2].count(AI) == 2 and P in board[2]
                    or col_row1.count(AI) == 2 and P in col_row1
                    or col_row2.count(AI) == 2 and P in col_row2):
                block_attempt = True
                logging.debug('block attempt detected')
            else:
                logging.debug('no block attempt made')

            if block_attempt is True:
                # it's a tarp!
                for row in range(3):
                    for col in range(3):
                        work_board = deepcopy(board)
                        chosen_cell = 'cell-{}:{}'.format(row, col)
                        if work_board[row][col] != '':
                            logging.debug('%s is occupied, moving on', chosen_cell)
                            continue
                        elif _is_edge(chosen_cell):
                            logging.debug('%s is an edge cell, moving on', chosen_cell)
                            continue

                        work_board[row][col] = AI

                        col_row1 = (work_board[0][0], work_board[1][0], work_board[2][0])
                        col_row2 = (work_board[0][2], work_board[1][2], work_board[2][2])
                        if (work_board[0].count(AI) == 2 and P not in work_board[0]
                                or work_board[2].count(AI) == 2 and P not in work_board[2]
                                or col_row1.count(AI) == 2 and P not in col_row1
                                or col_row2.count(AI) == 2 and P not in col_row2):
                            logging.debug('next ai move: %s', chosen_cell)
                            return chosen_cell
            else:
                # go for the win
                for row in range(3):
                    for col in range(3):
                        work_board = deepcopy(board)
                        chosen_cell = 'cell-{}:{}'.format(row, col)
                        if work_board[row][col] != '':
                            logging.debug('%s is occupied, moving on', chosen_cell)
                            continue

                        work_board[row][col] = AI

                        col_row1 = (work_board[0][0], work_board[1][0], work_board[2][0])
                        col_row2 = (work_board[0][2], work_board[1][2], work_board[2][2])
                        diag_row1 = (work_board[0][0], work_board[1][1], work_board[2][2])
                        diag_row2 = (work_board[0][2], work_board[1][1], work_board[2][0])
                        if (work_board[0].count(AI) == 3
                                or work_board[1].count(AI) == 3
                                or work_board[2].count(AI) == 3
                                or col_row1.count(AI) == 3
                                or col_row2.count(AI) == 3
                                or diag_row1.count(AI) == 3
                                or diag_row2.count(AI) == 3):
                            logging.debug('next ai move: %s', chosen_cell)
                            logging.debug('ai wins')
                            return chosen_cell

    raise NotImplementedError
