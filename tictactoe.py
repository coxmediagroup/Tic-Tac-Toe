from random import shuffle, choice

class Minimax(object):
    MINIMAX_DEPTH = 2

    def __init__(self, board):
        self.board = board

    def _minimax(self, depth, player):
        """
        Implements minimax according to:
        http://www.ntu.edu.sg/home/ehchua/programming/java/JavaGame_TicTacToe_AI.html#show-toc
        """
        best_score = float('-inf') if player == self.board.CURRENT_PLAYER else float('inf')
        best_position = -1
        moves = self.board.get_legal_moves()

        if not moves or depth == 0:
            best_score = self._evaluate()
            return (best_score, best_position)

        for move in moves:
            # try move for the current player
            self.board.spaces[move] = player
            if player == self.board.CURRENT_PLAYER: 
                # this is the MAX
                current_score = self._minimax(depth - 1, self.board.WAITING_PLAYER)[0]
                if current_score > best_score:
                    best_score = current_score
                    best_position = move

            else:
                # MIN
                current_score = self._minimax(depth - 1, self.board.CURRENT_PLAYER)[0]
                if current_score < best_score:
                    best_score = current_score
                    best_position = move

            # make sure to undo the move
            self.board.spaces[move] = move

        return (best_score, best_position)

    def _evaluate(self):
        return sum(self._evaluate_line(position) 
                    for position in self.board.WINNING_POSITIONS)

    def _evaluate_line(self, position):
        """
        The heuristic evaluation function for the current board
        @Return +100, +10, +1 for EACH 3-, 2-, 1-in-a-line for computer.
               -100, -10, -1 for EACH 3-, 2-, 1-in-a-line for opponent.
               0 otherwise
        Calculates the score for a given position.
        @param position tuple (int, int, int) representing a winning line
        @return int
        """
        score = 0
        first_pos, second_pos, third_pos = position
        # first space
        if self.board.spaces[first_pos] == self.board.CURRENT_PLAYER:
            score = 1
        elif self.board.spaces[first_pos] == self.board.WAITING_PLAYER:
            score = -1
        # second space 
        if self.board.spaces[second_pos] == self.board.CURRENT_PLAYER:
            if score == 1: 
                score = 10
            elif score == -1:
                return 0
            else:
                score = 1
        elif self.board.spaces[second_pos] == self.board.WAITING_PLAYER:
            if score == -1:
                score = -10 
            elif score == 1:
                return 0
            else: 
                score = -1
        # third space
        if self.board.spaces[third_pos] == self.board.CURRENT_PLAYER:
            if score > 0:
                score *= 10
            elif score < 0:
                return 0
            else:
                score = 1
        elif self.board.spaces[third_pos] == self.board.WAITING_PLAYER:
            if score < 0:
                score *= 10
            elif score > 1:
                return 0
            else:
                score = -1
        return score

    def make_pick(self, player):
        """
        Calls _minimax function
        """
        # if no picks have been made, choose a random space
        if len(self.board.get_legal_moves()) == self.board.NUM_SPACES:
            return choice(range(self.board.NUM_SPACES))
        return self._minimax(self.MINIMAX_DEPTH, player)[1]


class Player(object):

    def __init__(self, board, symbol, name, is_human=True, ai_strat=None):
        self.board = board
        self.symbol = symbol 
        self.name = name
        self.is_human = is_human
        self.ai_strat = ai_strat 

    def _get_player_input(self):
        """
        Gets a players input.
        """
        while True:
            try:
                space_num = int(raw_input('Space Number?'))
            except ValueError:
                print('Invalid Space Number, Please choose again')
            else:
                if self.board.is_valid_space(space_num):
                    return space_num
                print('Invalid Space Number, Please choose again')

    def make_play(self):
        """
        Puts a play on the board.  If player is human player prompt for a 
        play space, else if it is computer player, use an ai_strat to 
        determine the play.
        """
        if self.is_human:
            # prompt for user input
            space_num = self._get_player_input()
        else:
            # computer will only choose a valid space,
            # no need to validate, just mark it
            space_num = self.ai_strat.make_pick(self)

        self.board.mark_space(space_num, self)
        return space_num

    def __str__(self):
        return '<Player: {} {}>'.format(self.name, self.symbol)


class Board(object):
    NUM_SPACES = 9
    WINNING_POSITIONS = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # cols
        (0, 4, 8), (2, 4, 6) # diagonals
    )
    CURRENT_PLAYER = None
    WAITING_PLAYER = None
    
    def __init__(self):
        self.spaces = list(range(self.NUM_SPACES))

    def get_legal_moves(self):
        """
        Generates a collection of all legal moves on this board.
        @return list of ints that represent legal move indexes
        """
        # if someone has won return empty list
        if self.get_win():
            return []
        return [space for space in self.spaces if not isinstance(space, Player)]

    def get_win(self, player=None):
        """
        Checks if the board has any wins on it.
        If player is a Player instance it will only look to see if that player won.
        @return tuple (winning_positions_tuple, winning_player)
        """
        player = player or Player
        # go through each winning positions and check to see if
        # any of the positions have the same player instance
        for position in self.WINNING_POSITIONS:
            if (isinstance(self.spaces[position[0]], player) and
                self.spaces[position[0]] == self.spaces[position[1]] == self.spaces[position[2]]):

                return (position, self.spaces[position[1]])

        return False

    def is_valid_space(self, space_num):
        """
        Checks if a space is valid.
        Valid spaces must be an index in self.spaces, 
        and the space must be open.
        """
        return (space_num in range(self.NUM_SPACES) and
                self.is_space_open(space_num))

    def is_space_open(self, space_num):
        """
        Checks if a given space is open or not
        @return boolean
        """
        return not isinstance(self.spaces[space_num], Player)

    def mark_space(self, space_num, player):
        """
        Marks a space, on the board for the given player.
        @param player object Player instance
        """
        self.spaces[space_num] = player

    def __str__(self):
        """
        Prints board as a grid.
        """
        return """
        |{}|
        |{}|
        |{}|
        """.format(
            '|'.join(x.symbol if isinstance(x, Player) else str(x)
                        for x in self.spaces[:3]),
            '|'.join(x.symbol if isinstance(x, Player) else str(x)
                        for x in self.spaces[3:6]),
            '|'.join(x.symbol if isinstance(x, Player) else str(x)
                        for x in self.spaces[6:9]),
        )


def main():
    board = Board()
    players = [
        Player(board, 'H', 'human'),
        Player(board, 'C', 'computer', is_human=False, ai_strat=Minimax(board))
    ]
    # randomly determine who goes first
    shuffle(players)
    print(board)

    # game loop
    while True:
        # each player plays until the game has a winner
        for player in players:
            # always keep track of the active and waiting players
            board.CURRENT_PLAYER = player
            board.WAITING_PLAYER = players[1] if players.index(player) == 0 else players[0]
            print("{}'s Turn ({}):".format(player.name, player.symbol))
            player.make_play()
            print(board)

            # check to see if this game is over, 
            # if its not goes to next player's pick
            win = board.get_win()
            # A tie is when no one has won and all the legal moves are used up.
            if not win and not board.get_legal_moves():
                print('Tie!!!')
                return     
            elif win:
                print('{} Won! Game Over'.format(win[1].name))
                return

if __name__ == '__main__':
    main()
