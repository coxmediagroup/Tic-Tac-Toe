'''
INVINCITRON, an opponent that can win *all games* with 100% certainty [1]

Note [1]: current implementation only plays tic-tac-toe, future versions will expand on this.



'''

'''
Intructions:
1. Fork this repo on github.
2. Create an app that can interactively play the game of Tic Tac Toe against another player and never lose.
3. Commit early and often, with good messages.
4. Push your code back to github and send me a pull request.
'''


'''
Strategy

A player can play perfect tic-tac-toe (win or draw) given they move according to the highest possible move from the following table.[4]
Win: If the player has two in a row, play the third to get three in a row.
Block: If the opponent has two in a row, play the third to block them.
Fork: Create an opportunity where you can win in two ways.
Block opponent's fork:
Option 1: Create two in a row to force the opponent into defending, as long as it doesn't result in them creating a fork or winning. For example, if "X" has a corner, "O" has the center, and "X" has the opposite corner as well, "O" must not play a corner in order to win. (Playing a corner in this scenario creates a fork for "X" to win.)
Option 2: If there is a configuration where the opponent can fork, block that fork.
Center: Play the center.
Opposite corner: If the opponent is in the corner, play the opposite corner.
Empty corner: Play in a corner square.
Empty side: Play in a middle square on any of the 4 sides.
The first player, whom we shall designate "X", has 3 possible positions to mark during the first turn. Superficially, it might seem that there are 9 possible positions, corresponding to the 9 squares in the grid. However, by rotating the board, we will find that in the first turn, every corner mark is strategically equivalent to every other corner mark. The same is true of every edge mark. For strategy purposes, there are therefore only three possible first marks: corner, edge, or center. Player X can win or force a draw from any of these starting marks; however, playing the corner gives the opponent the smallest choice of squares which must be played to avoid losing.[5]
The second player, whom we shall designate "O", must respond to X's opening mark in such a way as to avoid the forced win. Player O must always respond to a corner opening with a center mark, and to a center opening with a corner mark. An edge opening must be answered either with a center mark, a corner mark next to the X, or an edge mark opposite the X. Any other responses will allow X to force the win. Once the opening is completed, O's task is to follow the above list of priorities in order to force the draw, or else to gain a win if X makes a weak play.

'''


# ttt has small state, so we can throw it around.  

def choose_move(game,player):
    pass


def game_is_won(game):
    ''' return play who wins the game, or False '''
    

## all of these are brute force.  We could save state along the way.
def can_win(game,player):
    pass

def can_block(game,player):
    pass

def can_fork(game,player):
    pass

def block_fork(game,player):
    pass

def center(game,player):
    pass

def opposite_corner(game,player):
    pass

def empty_corner(game,player):
    pass

def empty_side(game,player):
    pass

def random_move(game,player):
    pass

def suggest_optimal_move(game,player):
    move = None
    move_fns = (can_win,can_block,can_fork,
        block_fork,center,
        opposite_corner, empty_corner
        empty_side)
    while not move:
        for move_fn in move_fns:
            move = move_fn(game,player)

    return move

        



class Game(object):
    def __init__(self,):

    def move(player,position):
        


if __name__ == '__main__':
    interactive()









