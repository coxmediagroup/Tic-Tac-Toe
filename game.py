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


class NoWinningMove(Exception):
    pass


class Board(object):
    def __init__(self, player_cells, ai_cells):
        self.player_cells = player_cells
        self.ai_cells = ai_cells

        self.board = deepcopy(CLEAN_BOARD)
        for cell in player_cells:
            row, col = cell.replace('cell-', '').split(':')
            self.board[int(row)][int(col)] = P
        for cell in ai_cells:
            row, col = cell.replace('cell-', '').split(':')
            self.board[int(row)][int(col)] = AI

        self._workboard = deepcopy(self.board)

    @property
    def ai_first(self):
        return len(self.ai_cells) + 1 > len(self.player_cells)

    @property
    def turn(self):
        return len(self.player_cells) + len(self.ai_cells) + 1

    @property
    def block_attempt(self):
        results = filter(
            None,
            map(
                lambda x: x.count(AI) == 2 and P in x,
                [self.row1, self.row3, self.col1, self.col3],
            ),
        )
        return len(results) > 0

    @property
    def potential_win(self):
        results = filter(
            None,
            map(
                lambda x: x.count(P) == 2 and P not in x,
                [self.row1, self.row2, self.row3, self.col1, self.col2, self.col3, self.diag1, self.diag2],
            ),
        )
        return len(results) > 0

    @property
    def row1(self):
        return tuple(self._workboard[0])

    @property
    def row2(self):
        return tuple(self._workboard[1])

    @property
    def row3(self):
        return tuple(self._workboard[2])

    @property
    def col1(self):
        return (self._workboard[0][0], self._workboard[1][0], self._workboard[2][0])

    @property
    def col2(self):
        return (self._workboard[0][1], self._workboard[1][1], self._workboard[2][1])

    @property
    def col3(self):
        return (self._workboard[0][2], self._workboard[1][2], self._workboard[2][2])

    @property
    def diag1(self):
        return (self._workboard[0][0], self._workboard[1][1], self._workboard[2][2])

    @property
    def diag2(self):
        return (self._workboard[0][2], self._workboard[1][1], self._workboard[2][0])

    @property
    def workboard(self):
        return self._workboard

    def is_corner(self, cell):
        return cell in ['cell-0:0', 'cell-0:2', 'cell-2:0', 'cell-2:2']

    def is_edge(self, cell):
        return cell in ['cell-0:1', 'cell-1:0', 'cell-1:2', 'cell-2:1']

    def is_center(self, cell):
        return cell == 'cell-1:1'

    def block_win(self):
        for row in range(3):
            for col in range(3):
                self.reset_workboard()
                chosen_cell = 'cell-{}:{}'.format(row, col)
                if self.workboard[row][col] != '':
                    logging.debug('%s is occupied, moving on', chosen_cell)
                    continue

                self.workboard[row][col] = AI

                results = filter(
                    None,
                    map(
                        lambda x: x.count(P) == 2 and AI in x,
                        [self.row1, self.row2, self.row3, self.col1, self.col2, self.col3, self.diag1, self.diag2],
                    ),
                )
                if len(results) > 0 and not self.potential_win:
                    logging.debug('next ai move: %s', chosen_cell)
                    return chosen_cell

    def determine_corner_move(self):
        for row in range(3):
            for col in range(3):
                self.reset_workboard()
                chosen_cell = 'cell-{}:{}'.format(row, col)
                if self.workboard[row][col] != '':
                    logging.debug('%s is occupied, moving on', chosen_cell)
                    continue
                elif self.is_edge(chosen_cell):
                    logging.debug('%s is an edge cell, moving on', chosen_cell)
                    continue

                self.workboard[row][col] = AI

                results = filter(
                    None,
                    map(
                        lambda x: x.count(AI) == 2 and P not in x,
                        [self.row1, self.row3, self.col1, self.col3],
                    ),
                )
                if len(results) > 0:
                    logging.debug('next ai move: %s', chosen_cell)
                    return chosen_cell

        raise NotImplementedError

    def determine_straight_diagonal(self, cell):
        for row in range(3):
            for col in range(3):
                self.reset_workboard()
                chosen_cell = 'cell-{}:{}'.format(row, col)
                if self.workboard[row][col] != '':
                    logging.debug('%s is occupied, moving on', chosen_cell)
                    continue
                elif self.is_edge(chosen_cell):
                    logging.debug('%s is an edge cell, moving on', chosen_cell)
                    continue

                self.workboard[row][col] = AI

                if (self.diag1.count(AI) == 2
                        or self.diag2.count(AI) == 2):
                    logging.debug('next ai move: %s', chosen_cell)
                    return chosen_cell

    def determine_win_move(self):
        for row in range(3):
            for col in range(3):
                self.reset_workboard()
                chosen_cell = 'cell-{}:{}'.format(row, col)
                if self.workboard[row][col] != '':
                    logging.debug('%s is occupied, moving on', chosen_cell)
                    continue

                self.workboard[row][col] = AI

                if (self.row1.count(AI) == 3
                        or self.row2.count(AI) == 3
                        or self.row3.count(AI) == 3
                        or self.col1.count(AI) == 3
                        or self.col2.count(AI) == 3
                        or self.col3.count(AI) == 3
                        or self.diag1.count(AI) == 3
                        or self.diag2.count(AI) == 3):
                    logging.debug('next ai move: %s', chosen_cell)
                    logging.debug('ai wins')
                    return chosen_cell

        raise NoWinningMove

    def reset_workboard(self):
        self._workboard = deepcopy(self.board)

    def winning_cells(self):
        if self.row1.count(AI) == 3:
            return ('cell-0:0', 'cell-0:1', 'cell-0:2')
        elif self.row2.count(AI) == 3:
            return ('cell-1:0', 'cell-1:1', 'cell-1:2')
        elif self.row3.count(AI) == 3:
            return ('cell-2:0', 'cell-2:1', 'cell-2:2')
        elif self.col1.count(AI) == 3:
            return ('cell-0:0', 'cell-1:0', 'cell-2:0')
        elif self.col2.count(AI) == 3:
            return ('cell-0:1', 'cell-1:1', 'cell-2:1')
        elif self.col3.count(AI) == 3:
            return ('cell-0:2', 'cell-1:2', 'cell-2:2')
        elif self.diag1.count(AI) == 3:
            return ('cell-0:0', 'cell-1:1', 'cell-2:2')
        elif self.diag2.count(AI) == 3:
            return ('cell-0:2', 'cell-1:1', 'cell-2:0')


def ai_move_one():
    choices = ['cell-0:0', 'cell-0:2', 'cell-1:1', 'cell-2:0', 'cell-2:2']
    return choice(choices)


def calc_ai_move(player_cells, ai_cells):
    board = Board(player_cells, ai_cells)

    logging.debug('ai_first: %s', board.ai_first)
    logging.debug('turn: %s', board.turn)

    if board.turn == 3:
        if board.is_corner(ai_cells[0]) and not board.is_center(player_cells[0]):
            logging.debug('ai started in corner cell')
            logging.debug('player chose non-center cell as first move')
            chosen_cell = board.determine_corner_move()
            return dict(cell=chosen_cell)
        elif board.is_corner(ai_cells[0]):
            logging.debug('ai started in corner cell')
            logging.debug('player chose center cell as first move')
            chosen_cell = board.determine_straight_diagonal(ai_cells[0])
            return dict(cell=chosen_cell)

    elif board.turn == 5:
        if board.is_corner(ai_cells[0]) and not board.is_center(player_cells[0]):
            logging.debug('ai started in corner cell')
            logging.debug('checking for block attempt')

            if board.block_attempt is True:
                logging.debug('block attempt detected')
                # it's a tarp!
                chosen_cell = board.determine_corner_move()
                return dict(cell=chosen_cell)
            else:
                logging.debug('no block attempt made')
                # go for the win
                chosen_cell = board.determine_win_move()
                winning_cells = board.winning_cells()
                return dict(
                    cell=chosen_cell,
                    victor='ai',
                    winning_cells=winning_cells,
                )
        elif board.is_corner(ai_cells[0]):
            logging.debug('ai started in corner cell')
            logging.debug('player chose center cell as first move')
            # every move is a counter
            chosen_cell = board.block_win()
            return dict(cell=chosen_cell)

    elif board.turn == 7:
        if board.is_corner(ai_cells[0]):
            logging.debug('ai started in corner cell')
            # TODO: catch NoWinningMove and handle tie game
            chosen_cell = board.determine_win_move()
            winning_cells = board.winning_cells()
            return dict(
                cell=chosen_cell,
                victor='ai',
                winning_cells=winning_cells,
            )

    raise NotImplementedError
