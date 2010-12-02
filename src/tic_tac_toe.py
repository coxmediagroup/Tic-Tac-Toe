class TicTacToe(object):
   def __init__(self):
	self.reset_all()

   def reset_all(self):
	self.game_board=self.new_board()
	self.cell_states={"X":"X", "O":"O", "mt":" "}
	self.players= ["Droid1", "Droid2"]
	self.players_map= {"X":self.players[0], "O":self.players[1]}
	self.pieces= {"X":"X", "O":"O"}
	self.last_mover=None
	#self.playing= False
	#self.completed_moves= 0

   def get_display(self):
	b=self.game_board
	display="\n"+\
		b[0]+"|"+b[1]+"|"+b[2]+"\n"+\
		"-----\n"+\
		b[3]+"|"+b[4]+"|"+b[5]+"\n"+\
		"-----\n"+\
		b[6]+"|"+b[7]+"|"+b[8]+"\n"
	return display

   def get_board(self):
	return self.game_board

   def new_board(self):
	return ([
                '0','1','2',
                '3','4','5',
                '6','7','8'
                ])

   def reset_board(self):
	self.game_board=self.new_board()

   def set_player1(self, name):
	self.players[0]=name

   def set_player2(self, name):
	self.players[1]=name

   def get_player1(self):
	return self.__getplayer__(0)

   def get_player2(self):
	return self.__getplayer__(1)

   def __getplayer__(self, index):
	name=self.players[index]
	isadroid=name[0:len("droid")].lower()=="droid"
	return (name, isadroid)

   def __set_cell__(self, cell_id, state):
	valid_move=False
	if (0 <= cell_id < 9) \
		and (self.cell_states.has_key(state)) \
		and self.cell_is_mt(cell_id) \
		and self.get_winner()==None:
	   self.game_board[cell_id]=state
	   valid_move=True
	   self.set_lastmover()

	return valid_move

   def move(self, cell_id):
	if self.last_mover==None or self.last_mover==1:
	   state="X"
	else:
	   state="O"
	return self.__set_cell__(cell_id, state)

   def set_lastmover(self):
	if self.last_mover==None or self.last_mover==1:
	   self.last_mover=0
	elif self.last_mover==0:
	   self.last_mover=1

   def get_lastmover(self):
	if self.last_mover==None:
	   return None
	return self.players[self.last_mover]

   def cell_is_mt(self, number):
	return self.game_board[number] == str(number)

   def get_winner(self):
	winner=None
	b=self.game_board
        if b[3]==b[4]==b[5] or \
	   b[1]==b[4]==b[7] or \
	   b[0]==b[4]==b[8] or \
	   b[2]==b[4]==b[6]:
	      winner=self.players_map[b[4]]
        elif b[0]==b[1]==b[2] or \
		b[0]==b[3]==b[6]:
	  	   winner=self.players_map[b[0]]
	elif b[6]==b[7]==b[8] or \
		b[2]==b[5]==b[8]:
		   winner=self.players_map[b[8]]
	return winner
	   
class TicTacToeController(object):
   def __init__(self):
	self.game=TicTacToe()
	self.droid1_skill="high" #"low", "medium", or "high"
	self.droid2_skill="low" #"low", "medium", or "high"
	self.droid_predictability="high" #"low", "medium", or "high"
	self.gameTypes={"dvd":"(dvd) Droid1 vs. Droid2",
			"dvp":"(dvp) Droid vs. Player--- Droid moves first",
			"pvd":"(pvd) Player vs. Droid --- Player moves first",
			"pvp":"(pvp) Player1 vs. Player2"}
	self.gameTypeToPlayers={"dvd":("Droid1", "Droid2"),
				"dvp":("Droid", "Player"),
				"pvd":("Player", "Droid"),
				"pvp":("Player1", "Player2")
				}
	self.gameType=self.set_gameType("dvp")
	self.playerName=None

   def select_gameType(self):
	pass

   def set_gameType(self, selection):
	self.gameType=selection
	
def test1():
   c= TicTacToe()
   d= c.get_display()
   p1= c.get_player1()
   p2= c.get_player2()
   lm= c.get_lastmover()
   w=c.get_winner()
   c.set_player1("Michael")
   c.set_player2("Anthony")
   p12= c.get_player1()
   p22= c.get_player2()

   c.__set_cell__(0,"X")
   c.move(0)
   #c.__set_cell__(1,"O")
   c.move(1)
   #c.__set_cell__(3,"X")
   c.move(3)
   w2=c.get_winner()
   #c.__set_cell__(4,"O")
   c.move(4)
   #c.__set_cell__(6,"X")
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
test1()
