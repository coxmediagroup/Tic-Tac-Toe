from tic_tac_toe import TicTacToe
from tic_tac_toe import TicTacToeController

##################
#TEST STUFF BELOW#
##################
def test1(c):
   #c= TicTacToe()
   print "#############################\n"*3
   print c.get_pairs()
   print c.get_potentialwinningmoves("X",2), "pwm1"
   d= c.get_display()
   p1= c.get_player1()
   p2= c.get_player2()
   lm= c.get_lastmover()
   w=c.get_winner()
   c.set_player1("Michael")
   c.set_player2("Anthony")
   p12= c.get_player1()
   p22= c.get_player2()

   #c.__set_cell__(0,"X")
   c.move(0)
   #c.__set_cell__(1,"O")
   c.move(1)
   #c.__set_cell__(3,"X")
   c.move(3)
   w2=c.get_winner()
   #c.__set_cell__(4,"O")
   c.move(4)
   #c.__set_cell__(6,"X")
   print c.get_potentialwinningmoves("X",2), "pwm2"
   wm=c.get_winningmove("X")
   c.move(6)
   w3=c.get_winner()
   d2= c.get_display()

   c.reset_board()
   d3=c.get_display()

   print d
   print p1
   print p2
   print lm
   print w, "w"
   print p12
   print p22
   print w2, "w2", w3, "w3"
   print d2
   print d3

   print wm, "wm"

   c.move(8)
  
def test3():
	ttt= TicTacToe()
	control=TicTacToeController(ttt)

	player1=control.smart_generator_X()
        #player1=control.easy_generator()

	player2=control.good_generator_XO("O")
	#player2=control.easy_generator()

	print control.game.get_display()
	count=0
        while not control.game.hasa_winner() and count < 10:
		p1move=player1.next()
		control.game.move(p1move)
		count+=1
		if (not control.game.hasa_winner()):
			p2move=player2.next()
			control.game.move(p2move)
			count+=1
		print control.game.get_display()

        #print control.game.get_display()
test3()
#c= TicTacToe()
#test1(c)
#c.reset_all()
#test1(c)
#print c.get_Xmoves()
#print c.get_Omoves()
#print c.get_emptycells()
