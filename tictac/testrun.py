import board
import game
import pprint

pp = pprint.PrettyPrinter(indent=4)
g = board.TTTGameBoard(board='x--o--x--', active_player='o')

gs = game.get_next_gamestate(g)
print "Final:\n"
print gs
