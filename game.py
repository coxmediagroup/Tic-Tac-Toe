#! /usr/bin/env python
from bitarray import bitarray
from exceptions import Exception
from optparse import OptionParser

import sys

if not sys.version_info[:2] == (2, 7):
    print "Warning, this script has only been tested with python 2.7"

row_wins = (bitarray('111000000'), bitarray('000111000'), bitarray('000000111'))
col_wins = (bitarray('100100100'), bitarray('010010010'), bitarray('001001001'))
diag_wins =(bitarray('100010001'), bitarray('001010100'))

wins = row_wins + col_wins + diag_wins
row_dict = {'a':0, 'b':3, 'c': 6}
col_dict = {'1': 0, '2':2, '3':2}

if __file__ == "__main__":
    print "error"
    parser = OptionParser()
    parser.add_option("-f", "--file",
                      help="read game moves from a file", metavar="FILE")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose",
                      help="Print additional messages to the user", default=False)
    (options, args) = parser.parse_args()

class InvalidMove(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class TicTacToe(object):
    ''' This is the Game
    '''
    player_one = bitarray('000000000') # machine
    player_two = bitarray('000000000') # opponent
    blank_board =  bitarray('000000000')

    def board(self):
        return self.player_one | self.player_two

    def reset(self):
        self.player_one = bitarray('000000000') # machine
        self.player_two = bitarray('000000000') # opponent

    def parse_move(self, move):
        if len(move)!=2:
            raise InvalidMove(move)
        try:
            return row_dict[move[0]], col_dict[move[1]]
        except KeyError:
            raise InvalidMove(move)

    def move(self, player, move):
        row, col = self.parse_move(move)
        if self.board()[row+col]==True :
            return False
        player[row+col]=True
        return True

    #TODO: Should remove legal_move function
    """
    def legal_move(self, move):
        row, col = self.parse_move(move)
        try:
            if self.board()[row+col]==False:
                return True
        except:
            return False
        return False

    #TODO: Should remove is_there_a_winner function
    def is_there_a_winner(self):
        for win in wins:
            if (win & self.player_one)==win:
                return self.player_one, win
            if (win & self.player_two)==win:
                return self.player_two, win
        return False
    """

    def is_it_a_winner(self, player):
        """Does this player have a winner"""
        for win in wins:
            if (win & player)==win:
                return True
        return False

    def choose_move(self, player, offset=0):
        '''simplest solution first, find the first empty cell'''
        for a_index in range(0, len(player)):
            position = (a_index + offset) % 9
            if self.board()[position] is False:
                player[position] = True
                return True
        return False #no moves left

    def may_move_lead_to_win(self, move, player):
        '''check if all possible rows, columns or  diags are blocked
        '''
        pass

    def possible_moves(self, board=None):
        """What moves are available."""
        if board is None:
            board = self.board()
        choices = []
        for position in range(0, 9):
            if board[position]==False:
                choices.append(position)
        return choices

    def is_there_a_winning_move(self, player, optional_block = -1):
        """If there is such a move return it. Otherwise return false."""
        t_play = player
        pos = self.possible_moves()
        for position in pos:
            if position == optional_block:
                continue
            t_play[position] = True
            if self.is_it_a_winner(t_play):
                t_play[position] = False
                return position
            t_play[position] = False
        return False

    def move_that_results_with_two_winning_options(self, player):
        """If there is such a move return it. Otherwise return false."""
        choices = self.possible_moves()
        count = 0
        for choice in choices:
            player[choice] = True
            result = self.is_there_a_winning_move(player)
            if result is not False:
                count += 1
                """Check for another winning play using this move"""
                result = self.is_there_a_winning_move(player, result)
                if result is not False:
                    player[choice] = False
                    return choice
            player[choice] = False
        return False

    def wins_for_position(self, position):
        p_wins = []
        for w in wins:
            if w[position] == True:
                p_wins.append(w)
        return p_wins

    def most_winning_options(self, player):
        """
        player is opposing player
        """
        choices = self.possible_moves()
        win_count_for_choice = {}
        best = (choices[0], 0)
        for choice in choices:
            """find wins"""
            wins_for_choice = self.wins_for_position(choice)
            win_count = 0
            for w in wins_for_choice:
                if w & player==bitarray('000000000'):
                    win_count += 1
            if win_count>best[1]:
                best = (choice, win_count)
        return best

    def make_the_best_move(self):
        """Find the best possible move. Start by checking if there is a winning move for us"""
        #pdb.set_trace()
        result = self.is_there_a_winning_move(self.player_one)
        if result is not False:
            self.player_one[result] = True
            return result
        '''Check if opponent has a winning move, if so block it'''
        result = self.is_there_a_winning_move(self.player_two)
        if result is not False:
            self.player_one[result] = True
            return result
        '''Is there a move that gives two immediate chances to win'''
        result = self.move_that_results_with_two_winning_options(self.player_one)
        if result is not False:
            self.player_one[result] = True
            return result
        '''Does the opponent have a move that will give them two chance'''
        result = self.move_that_results_with_two_winning_options(self.player_two)
        if result is not False:
            self.player_one[result] = True
            return result
        '''Find the move that gives us the most chances to win and our opponent the least '''
        my_best_move, my_win_count = self.most_winning_options(self.player_two)
        opponents_best_move, opp_win_count = self.most_winning_options(self.player_two)
        if (my_win_count + opp_win_count)==0:
            return False
        if my_win_count>=opp_win_count:
            self.player_one[my_best_move] = True
            return (my_best_move, my_win_count)
        else:
            self.player_one[opponents_best_move] = True
            return (opponents_best_move, opp_win_count)


def main(options, args):
    print """
            please designate your move by entering a row('abc') and column('123')
            for example the top left corner would be designated as 'a1'
            print "your moves would be designated, by an 'X', and the computers by a 'Y'
          """
    s = raw_input('---->')



if __file__ == "__main__":
    print "start"
    parser.parse_args()
    main()
