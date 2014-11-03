import board
import bot 
import pprint

pp = pprint.PrettyPrinter(indent=4)
g = board.TTTGameBoard(board='---------', active_player='x')
g = board.TTTGameBoard(board='x--o-ox--', active_player='x')

print g
while g.depth < 9 and g.winner is None:
    g = bot.get_next_gamestate(g)
    print g
    print g.friendly_board()
