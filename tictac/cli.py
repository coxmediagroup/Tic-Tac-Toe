"""
    Command line interface for computer vs. bot, bot vs bot and bot vs. random
    Tic Tac Toe game.

    Board implemented in board.py

    Bot implemented in bot.py

"""

import random
import sys

import board
import bot


class TTTGameLoop(object):

    def __init__(self):
        self.game = board.TTTGameBoard()
        self.gametype = 1

    #get the next move from the list of available moves
    def get_move(self):
        move = None
        while move is None:
            print "\n---------"
            print "Please select an open square from those numbered below:"
            print self.game.friendly_board()
            print "Legal moves: {}".format(self.game.get_legal_moves())
            print "---------"
            move = raw_input("What move would you like to make? ")

            if not move.isdigit() or int(move) not in self.game.get_legal_moves():
                print "\nERROR"
                print "'{}' is an invalid move.".format(move)
                move = None
            else:
                return int(move) 


    #get the next move for the AI
    def get_move_bot(self):
        next_gamestate = bot.get_next_gamestate(self.game)
        print "The Bot (playing as {}) chooses square {}.".format(
                self.game.active_player.upper(),
                next_gamestate.last_move)
        return next_gamestate.last_move


    #get the next move for the Random AI
    def get_move_random(self):
        legal_moves = self.game.get_legal_moves()
        move = legal_moves[random.randint(0,len(legal_moves)-1)]
        print "The Crazy Bot (playing as {}) chooses square {}.".format(
                self.game.active_player.upper(),
                move)
        return move
        

    # get the type of game
    def get_gametype(self):
        gametype = None
        print "Would you like to play a game?"
        while gametype is None:
            print "\n---------"
            print "Game Types Available:"
            print "    1.) Player vs. Bot"
            print "    2.) Bot vs. Bot"
            print "    3.) Bot vs. Crazy Bot (Random)"
            print "    4.) I don't want to play a game."
            print "---------\n"
            gametype = raw_input("What type of game would you like to play? ")

            if not gametype.isdigit() or int(gametype) not in [1,2,3,4]:
                print "\nERROR"
                print "'{}' is an invalid game type.".format(gametype)
                gametype = None
            else:
                return int(gametype)
    
    def declare_winner(self):
        print "Game Over!  Final board:"
        print self.game.friendly_board() 
        if self.game.winner:
            print "{} is the winner!".format(self.game.winner.upper())
        else:
            print "No one won.  Good game!"
        sys.exit()

    def run(self):
        gametype = self.get_gametype()
        # single player
        # bot v bot
        # bot v random

        #display the open board
        print self.game.friendly_board()

        #if the player is playing, choose which side 
        #if the AI is playing vs random, this will act as the random turn
        player_turn = random.choice(['x','o'])
        if gametype == 1:
            print "\nWe flipped a coin, you're playing as {}!".format(player_turn.upper())

        if gametype == 4:
            print "\nYou're right.  The only way to win is not to play.  Goodbye!"
            sys.exit()

        #while there is no winner and there are still legal moves
        while self.game.winner is None and len(self.game.get_legal_moves()) > 0:

            #if it's the AIs turn, or if it's AI vs AI
            if gametype == 2 or player_turn != self.game.active_player:
                move = self.get_move_bot()
                self.game = self.game.apply_move(move)
                if gametype == 2:
                    print self.game.friendly_board()
                continue

            #if it's player v  bot and it's the player's turn, ask them
            if gametype == 1 and player_turn == self.game.active_player:
                move = self.get_move()
                self.game = self.game.apply_move(move)
                continue

            #if it's bot v random and it's the random's turn, roll it
            if gametype == 3 and player_turn == self.game.active_player:
                move = self.get_move_random()
                self.game = self.game.apply_move(move)
                print self.game.friendly_board()
                continue

        self.declare_winner()
