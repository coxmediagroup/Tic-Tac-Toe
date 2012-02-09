
from game.models import Game, PLAYER_X, PLAYER_O, PLAYER_NONE

class Computer(object):
    @classmethod
    def determine_move(cls, game, comp, user):
        assert comp == PLAYER_X or comp == PLAYER_O
        assert game.who_moves() == comp

        move = game.winning_move(for_player=comp)
        if move is None:
            move = game.winning_move(for_player=user)
            if move is None:
                # if there are no winning moves
                if game[1][1] == PLAYER_NONE:
                    # take the center if it's available
                    move = (1,1)
                else:
                    # since the center is taken,look for the user's token
                    # and play next to it
                    for x,y in ((x,y) for y in range(0,3) for x in range(0,3)):
                        if game[x][y] == user:
                            if x == 1 and y == 1:
                                continue #ignore the center
                            elif x < 2 and game[x+1][y] == PLAYER_NONE:
                                move = (x+1,y)
                                break
                            elif y < 2 and game[x][y+1] == PLAYER_NONE:
                                move = (x,y+1)
                                break
                            elif x > 0 and game[x-1][y] == PLAYER_NONE:
                                move = (x-1,y)
                                break
                            elif y > 0 and game[x][y-1] == PLAYER_NONE:
                                move = (x,y-1)
                                break
                    else:
                        # we have arrived here because only 
                        # the center is occupied
                        move = (0,0)
        assert move is not None
        
        return move

