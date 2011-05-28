import time
import random
import math


class Board(object):
    """
    This class represents a basic game board. The cells will hold either X or O, or None
    if a player has not played it yet.
    Arguments allow you to load the state of a board.
    """
    def __init__(self, cells = None, history = None):
        self._move_cache = None
        self.history = [] if history is None else history

        if cells is None:
            self._cells = []
            for i in range(0, 3):
                self._cells.append([None]*3)
        else:
            self._cells = cells
        
    def dump_state(self):
        return (self._cells, self.history)

    def output(self):
        for row in self._cells:
            for cell in row:
                if cell is None: 
                    print '%02s'%'-',
                else:
                    print '%02s'%cell,
            print '\n'

    def get_val(self, x, y):
        return self._cells[y][x]

    def set_val(self, x, y, val):
        self._move_cache = None
        if self._cells[y][x] != val:
            #only set/keey history if the cell has changed.
            self._cells[y][x] = val
            self.history.append(((x, y), val))

    def get_valid_moves(self):
        """
        Returns a list of valid moves left (without an X or an O in them)
        Will not compute itself twice without a set_val
        """
        if self._move_cache:
            return self._move_cache

        out = []
        for y, row in enumerate(self._cells):
            for x, cell in enumerate(row):
                if cell == None:
                    out.append((x, y))
        self._move_cache = out
        return out

    def get_locations(self, val):
        """
        Returns all coordinates that hold value val
        """
        locations = []
        for y, row in enumerate(self._cells):
            for x, cell in enumerate(row):
                if val == cell:
                    locations.append((x, y))

        return locations

X_TRANSFORM = [[2, 1, 0], [1, 0, -1], [0, -1, -2]]
Y_TRANSFORM = [[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]

def rotate(board, turns=1):
    #turns a board clockwise by turns turns
    if turns == 0:
        return board
    newboard = Board()
    for y, row in enumerate(board._cells):
        for x, cell in enumerate(row):
            xtrans = X_TRANSFORM[y][x]
            ytrans = Y_TRANSFORM[y][x]
            newboard.set_val(x + xtrans, y + ytrans, cell)
    return rotate(newboard, turns-1)

def rotate_cell(cell, turns=1):
    #rotates cell coordinates as if it were in a rotated board
    if turns == 0:
        return cell
    x, y = cell
    xtrans = X_TRANSFORM[y][x]
    ytrans = Y_TRANSFORM[y][x]
    return rotate_cell((x+xtrans, y+ytrans), turns-1)

    
class Player(object):
    """
    Base class for either human or computer based player.
    """
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.avatar = 'X' if player == 1 else 'O'

    def get_move(self):
        board = self.game.board
        """
        Returns a tuple of board coordinates (x,y)
        This is a very simple implementation to be overwritten by child classes
        """
        print "Please enter coordinates for a move in form of (x, y) for %s"%self.avatar
        try:
            move = eval(raw_input())
        except:
            print "Invalid input"
            return self.get_move()

        if move not in board.get_valid_moves() or not isinstance(move, tuple):
            print "Invalid move"
            return self.get_move()
        return move

DECISIONS = {
    "wentfirst": {
        "_action": "(0, 0)",
        "chose_center": {
            "_action": "(2, 2)",
            "chose_corner": "choose_corner",
            "chose_edge": "block_and_draw"
        },
        "chose_corner": {
            "_action": "choose_corner",
            "default": "choose_corner"
        },
        "chose_edge": {
            "_action": "choose_center",
            "threatens": "block_and_draw",
            "default": "choose_corner_not_bordered"
        }
    },
    "wentsecond": {
        "chose_center": {
            "_action":"choose_corner",
            "threatens": "block_and_draw",
            "default": "choose_corner"
        },
        "default": {
            "_action": "choose_center",
            "threatens": {
                "_action": "block",
                "threatens": "block_and_draw",
                "default": "choose_edge"
            },
            "two_corners": "choose_edge",
            "edge_borders_corner": "choose_bordered_corner",
            "edge_doesnt_border_corner": {
                "_action": "choose_edge",
                "default": "choose_corner_bordered_by_one_x"
            },
            "default": "choose_caddy_corner"
            
        }

    }
}
        
class Computer(Player):
    def __init__(self, *args, **kwargs):
        self.corners = [(0, 0), (2, 0), (0, 2), (2, 2)]
        self.edges = [(0, 1), (1, 2), (2, 1), (1, 0)]
        self.center = [(1, 1)]
        self.rotation = 0
        self.strategy = None
        super(Computer, self).__init__(*args, **kwargs)

    def _unrotate(self, move):
        if self.rotation == 0:
            return move
        return rotate_cell(move, 4-self.rotation)

    def _distance(self, p1, p2):
        #returns the distance between two points
        return math.sqrt(math.pow(p2[0]-p1[0], 2) + math.pow(p2[1]-p1[1], 2))

    def _is_adjacent(self, p1, p2):
        #checks if two squares directly border each other
        return abs(self._distance(p1, p2) - 1.0) < 0.01

    def _is_diagonal(self, p1, p2):
        #checks if two squares are diagional to each other
        return abs(self._distance(p1, p2) - 1.414) < 0.01

    def _get_bordered_corner(self, p1, p2):
        coords = [p1, p2]
        coords.sort() #want the lowest X first
        rotation = 0
        while coords != [(0,1), (1,0)]:
            rotation += 1
            coords[0] = rotate_cell(coords[0])
            coords[1] = rotate_cell(coords[1])
        return rotate_cell((0,0), 4-rotation)

    def get_move(self):
        board = self.game.board
        if len(board.history) == 0:
            #first move, choose a corner
            move = random.choice(self.corners)
            self.rotation = self._get_rotation(move)
            self.strategy = DECISIONS["wentfirst"]
            return move

        if len(board.history) == 1:
            self.strategy = DECISIONS["wentsecond"]

        last_move, player = board.history[-1]

        if self.rotation:
            board = rotate(board, self.rotation)
            last_move = rotate_cell(last_move, self.rotation)
            
        next_wins = self._check_for_win()
        if next_wins: #we won!
            return next_wins

        #variables used by filter functions
        opponent_avatar = 'X' if self.avatar == 'O' else 'O'
        opponent_coordinates = board.get_locations(opponent_avatar)
        valid_moves = board.get_valid_moves()

        """
        Logic filters to check conditions on the board
        #todo - move these out of this function
        """
        chose_center = lambda: last_move == (1,1)
        chose_corner = lambda: last_move in self.corners
        chose_edge = lambda: last_move in self.edges
        threatens = lambda: self._check_for_win(opponent_avatar)
        default = lambda: True
        two_corners = lambda: len([coord for coord in opponent_coordinates if coord in self.corners]) == 2
        block = lambda: threatens()
        def edge_borders_corner():
            edges = [coord for coord in opponent_coordinates if coord in self.edges]
            if len(edges) != 2:
                return False
            return self._is_diagonal(edges[0], edges[1])
        def edge_doesnt_border_corner():
            edges = [coord for coord in opponent_coordinates if coord in self.edges]
            if len(edges) != 2:
                return False
            return not(self.is_diagonal(edges[0], edges[1]))

        """
        Action functions
        #todo - move these out of this function
        """
        choose_corner = lambda: random.choice(list(set(self.corners).intersection(set(valid_moves))))
        choose_edge = lambda: random.choice(list(set(self.edges).intersection(set(valid_moves))))
        choose_center = lambda: (1,1)

        def choose_corner_not_bordered():
            #want a corner not bordered by an opponent
            edges = [coord for coord in opponent_coordinates if coord in self.edges]
            bordered_corner = self._get_bordered_corner(edges[0], edges[1])
            return [move for move in valid_moves if move in self.corners and move != bordered_corner][0]

        def choose_bordered_corner():
            #want the corner bordered by two opponents
            edges = [coord for coord in opponent_coordinates if coord in self.edges]
            bordered_corner = self._get_bordered_corner(edges[0], edges[1])
            return bordered_corner

        def choose_corner_bordered_by_one_x():
            #opponent just chose an edge to block, we want a corner on the other side
            opposite_edge = rotate_cell(last_move, 2)
            corner = [move for move in valid_moves if move in self.corners and move[0] == opposite_edge[0] or move[1] == opposite_edge[1]]
            return corner[0]

        def choose_caddy_corner():
            corner = [move for move in opponent_coordinates if move in self.corners][0]
            return rotate_cell(corner, 2)

        def block_and_draw():
            block = threatens()
            if block:
                return block
            return random.choice(valid_moves)
        
               

        """
        Begin strategy walking.
        As we advance the tree, self.strategy updates.
        block_and_draw is the only function that repeats itself. All others default to block_and_draw.
        If a result is a dictionary, _action is taken and the new strategy is set. Otherwise, it is checked
        for a coordinate then for a string (that translates to a function in this scope).
        """

        new_strategy = None
        if isinstance(self.strategy, dict):
            for f_name in [f_name for f_name in self.strategy if not f_name.startswith('_') and f_name != 'default']:
                f_func = eval(f_name)   
                if f_func():
                    new_strategy = self.strategy[f_name]
                    break

            if new_strategy is None:
                new_strategy = self.strategy.get('default', 'block_and_draw')
        else:
            new_strategy = 'block_and_draw'

        self.strategy = new_strategy
        if isinstance(self.strategy, dict):
            action = self.strategy.get('_action', 'block_and_draw')
        else:
            action = self.strategy

        move = eval(action)()

        block = threatens()
        if block and block != move:
            print "Problem in current logic, other player will win without block. Blocking."
            move = block

        
        return self._unrotate(move)
            
    def _get_rotation(self, move):
        rotation = 0
        while move not in set([(0,0), (0,1), (1,1)]):
            rotation += 1
            move = rotate_cell(move)
        return rotation
        
    def _check_for_win(self, avatar=None):
        """
        Checks for a circumstance where avatar can win with the next move
        """
        avatar = self.avatar if avatar is None else avatar
        for row in self.game.ranges:
            cells = self.game.get_row(row)
            if cells.count(avatar) == 2 and None in cells:
                #found a winning spot
                return self.game.ranges[row][cells.index(None)]
        return None
                    


class Game(object):
    """ 
    X(horizontal)/Y(vertical) Coordinates
      0   1   2
    0 X | X | X
    1 X | X | X
    2 X | X | X

    Row designations 
    6 3   4   5 7
    0 X | X | X
    1 X | X | X    
    2 X | X | X
    """

    def __init__(self, board, p1, p2):
        self.board = board
        self.p1 = p1(self, 1)
        self.p2 = p2(self, 2)
        self.turn = 1
        self.ranges = self._build_row_ranges()

    def get_row(self, row_number):
        return [self.board.get_val(*cell) for cell in self.ranges[row_number]]

    def _check_row_for_win(self, row):
        vals = [self.board.get_val(*cell) for cell in row]
        if vals == ['X']*3: return 'X'
        elif vals == ['O']*3: return 'O'
        return False
        
    def _build_row_ranges(self):
        #horizontal rows
        rows = {}
        for y in range(0,3):
            row = []
            for x in range(0,3):
                row.append((x,y))
            rows[y] = row

        #vertical rows
        for x in range(0,3):
            row_n = x + 3
            row = []
            for y in range(0, 3):
                row.append((x,y))
            rows[row_n] = row

        #diagonals
        for i in range(0,3):
            rows.setdefault(6, []).append((i,i))
            rows.setdefault(7, []).append((2-i, i))
        return rows

    def check_for_win(self):
        """Checks the board for a win. (via every possible row)"""
        for number, row in self.ranges.iteritems():
            win = self._check_row_for_win(row)
            if win:
                return (number, win)
        return False

    def start(self):
        while True:
            p = self.p1 if self.turn == 1 else self.p2
            avatar = 'X' if self.turn == 1 else 'O'
            print "Player %s's move"%avatar
            self.board.output()
            print
            move = p.get_move()
            self.board.set_val(move[0], move[1], avatar)
            win = self.check_for_win()
            if win:
                print "Player %d (%s's) won on row %d!"%(self.turn, avatar, win[0])
                print self.board.output()
                print
                return win
            if not self.board.get_valid_moves():
                print "Tie."
                print self.board.output()
                print
                return None

            self.turn = 2 if self.turn == 1 else 1

def main():
    random.seed(time.time())
    b = Board()
    p1 = None
    p2 = None
    g = Game(b, Computer, Player)
    g.start()
    

if __name__ == '__main__':
    main()


