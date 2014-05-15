'''
Created on Oct 16, 2012

@author: Josh
'''
import random
class Game(object):
    '''
    no time!
    '''
    def __init__(self):
        self.data = [[]]
        self.clear()
        
    def __repr__(self):
        result = ''
        for row in xrange(3):
            for column in xrange(3):
                square = self.data[column][row]
                if square == 0:
                    result += ' , '
                elif square == 1:
                    result += "O, "
                elif square == 2:
                    result += "X, "
            result = result[:-2]
            result = result + '\n'
    
        return result[:-1]
    
    def clear(self):
        self.active = True
        self.data = [[0 for __ in xrange(3)] for __ in xrange(3)]
        
    def get(self, c, r): 
        return self.data[c][r]
    
    def get_row(self, row):
        result = []
        for column in self.data:
            result.append(column[row])
        return result
    
    def get_column(self, col):
        return self.data[col]
    
    def get_diagonals(self):
        return [
            [self.data[0][0], self.data[1][1], self.data[2][2]],
            [self.data[2][0], self.data[1][1], self.data[0][2]]
        ]   
        
    def all_match(self, a_list):
        if len(a_list) <= 0: return False
        
        value = a_list[0]
        return len(filter(lambda x: x == value, a_list)) == len(a_list), value
        
    def game_over(self):
        for x in self.data:
            matches, value = self.all_match(x)
            if matches and value != 0: return True, value
            
            for y in x:
                matches, value = self.all_match(self.get_row(y))
                if matches and value != 0:
                    return True, value
    
        for line in self.get_diagonals():
            matches, value = self.all_match(line)
            if matches and value != 0:
                return True, value
            
        return self.number_of_empty_spaces() == 0, None
            
    def make_choice(self, column, row, choice):
        play_made = False
        if self.active and self.data[column][row] == 0:
            self.data[column][row] = choice
            play_made = True
        return play_made
    
    def number_of_empty_space_column(self, column):
        if column < 0 or column > 2: return 0
        
        n = 0
        for x in self.data[column]:
            if x == 0: n += 1
        return n
    
    def number_of_empty_spaces_row(self, row):
        if row < 0 or row > 2: return 0
        
        n = 0
        for y in self.get_row(row):
            if y == 0: n += 1
        return n
    
    def number_of_empty_spaces(self):
        n = 0;
        for x in xrange(3):
            for y in xrange(3):
                if self.data[x][y] == 0:
                    n += 1
        return n
            
    def make_ai_choice(self, choice):
        if not self.active or self.number_of_empty_spaces() == 0: 
            return 
        
        block = 1
        if choice == 1: block = 2
        
        # trying to win
        for column in self.data:
            if self.win_or_block(column, choice): return
                
        for row in xrange(3):
            if self.win_or_block_row(self.get_row(row), row, choice): return
            
        if self.win_or_block_diag(choice): return 
            
        # blocking now
        for column in self.data:
            if self.win_or_block(column, block, choice): return
            
        for row in xrange(3):
            if self.win_or_block_row(self.get_row(row), row, block, choice): return
            
        if self.win_or_block_diag(block, choice): return
        
        # only gets here early on! (and for the last move on a tie)
        return self.make_early_choice(choice)
    
    def win_or_block(self, column, target, block_with=None):
        if column[0] == target and column[1] == target and column[2] == 0:
            column[2] = block_with or target
            return True
        elif column[0] == target and column[1] == 0 and column[2] == target:
            column[1] = block_with or target
            return True
        elif column[0] == 0 and column[1] == target and column[2] == target:
            column[0] = block_with or target
            return True
        return False
            
    # I only have a few minutes to finish :/
    def win_or_block_row(self, row, row_number, target, block_with=None):
        if row[0] == target and row[1] == target and row[2] == 0:
            self.data[2][row_number] = block_with or target
            return True
        elif row[0] == target and row[1] == 0 and row[2] == target:
            self.data[1][row_number] = block_with or target
            return True
        elif row[0] == 0 and row[1] == target and row[2] == target:
            self.data[0][row_number]  = block_with or target
            return True
        return False
        
    # rule based decisions -- means lots of special cases...
    def win_or_block_diag(self, target, block_with=None):
        if self.data[0][0] == target and self.data[1][1] == target and self.data[2][2] == 0:
            self.data[2][2] = block_with or target
            return True
        elif self.data[0][0] == 0 and self.data[1][1] == target and self.data[2][2] == target:
            self.data[0][0] = block_with or target
            return True
        elif (self.data[0][0] == target and self.data[2][2] == target or \
             self.data[2][0] == target and self.data[0][2] == target) and self.data[1][1] == 0:
            self.data[1][1] = block_with or target
            return True
        elif self.data[0][2] == 0 and self.data[1][1] == target and self.data[2][0] == target:
            self.data[0][2] = block_with or target
            return True
        elif self.data[0][2] == target and self.data[1][1] == target and self.data[2][0] == 0:
            self.data[2][0] = block_with or target
            return True
        elif self.data[0][2] == target and self.data[1][1] == target and self.data[2][0] == 0:
            self.data[2][2] = block_with or target
            return True
        return False
    
    def get_corners_taken(self, choice):
        result = []
        
        # I am copying and pasting for speed here
        # you can see things more my style on my website: joshbyrom.com
        if self.data[0][0] != choice and self.data[0][0] != 0: 
            result.append((0, 0))
            
        if self.data[0][2] != choice and self.data[0][2] != 0:
            result.append((0, 2))
            
        if self.data[2][0] != choice and self.data[2][0] != 0: 
            result.append((2, 0))
            
        if self.data[2][2] != choice and self.data[2][2] != 0:
            result.append((2, 2))
            
        return result
    
    def __choose_one_near(self, x, y, choice):
        left = self.number_of_empty_space_column(x - 1)
        right = self.number_of_empty_space_column(x + 1)
        
        up = self.number_of_empty_spaces_row(y - 1)
        down = self.number_of_empty_spaces_row(y + 1)
        
        x_mod = 0
        y_mod = 0
        
        if left > right:
            x_mod = -1
            if up > left or down > left:
                x_mod = 0
        else:
            x_mod = 1
            if up > right or down > right:
                x_mod = 0
                
        if x_mod == 0:
            if up > down:
                y_mod = -1
            else:
                y_mod = 1
            
        if self.data[x + x_mod][y + y_mod] == 0:
            self.data[x + x_mod][y + y_mod] = choice
        return True
    
        return False
    
    def __choose_a_corner(self):
        choices = []
        if self.data[0][0] == 0:
            choices.append((2,2))
        elif self.data[2][0] == 0:
            choices.append((0, 2))
        elif self.data[0][2] == 0:
            choices.append((2, 0))
        elif self.data[2][2] == 0:
            choices.append((0, 0))
            
        for choice in choices:
            if self.data[choice[0]][choice[1]] == 0:
                return choice
        return None
            
    def make_early_choice(self, choice):
        corners = self.get_corners_taken(choice)
        if len(corners) >= 1:
            if self.data[1][1] == 0:
                self.data[1][1] = choice
                return True
            elif self.data[1][1] == choice:
                return self.__choose_one_near(1, 1, choice)
            else:   # they went center and now have a corner
                corner = self.__choose_a_corner()
                self.data[corner[0]][corner[1]] = choice
                return True
        elif self.data[1][1] != 0 and self.data[1][1] != choice:
            corner = self.__choose_a_corner()
            self.data[corner[0]][corner[1]] = choice
            return True
        else:   # take the center or something near it
            if self.data[1][1] == 0:
                self.data[1][1] = choice
                return True
            else:
                return self.__choose_one_near(1, 1, choice)
            
    
    def __choose_random(self):
        empty = []
        for column in xrange(3):
            for row in xrange(3):
                if self.data[column][row] == 0:
                    empty.append((column, row))
                    
        if len(empty) <= 0: # empty's empty!
            return None,
                    
        random.shuffle(empty)
        return empty[0][0], empty[0][1]
            
            
    def check_winner(self):
        over, winner = self.game_over()
        if over:
            print 'game over,', winner, 'wins'
            self.active = False
    
            
        