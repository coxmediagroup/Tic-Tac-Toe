class TicTacToe(object):
   def __init__(self):
	self.reset_all()

   def reset_all(self):
	self.game_board=self.new_board()
	self.cell_states={"x":"X", "o":"O", "mt":" "}
	self.players= ["Droid1", "Droid2"]
	self.pieces= {"x":"X", "o":"O"}
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
	return self.game_board=self.new_board()

   def set_player1(self, name):
	self.player[0]=name

   def set_player2(self, name):
	self.player[1]=name

   def set_cell(self, cell_id, state):
	valid_move=False
	if (0 <= cell_id < 9) \
		and (self.cell_states.has_key(state)) \
		and self.cell_is_mt(cell_id):
	   self.game_board(cell_id)=state
	   valid_move=True

	return valid_move

   def cell_is_mt(self, number):
	return self.cell_states[number] == str(number)
	   
class TicTacToeController(object):
   def __init__(self):
	self.game=TicTacToe()
	self.droid1_skill="high" #"low", "medium", or "high"
	self.droid2_skill="low" #"low", "medium", or "high"
	self.droid_predictability="high" #"low", "medium", or "high"
	self.gameTypes={"dvd":"(dvd) Droid vs. Droid",
			"dvp":"(dvp) Droid vs. Player--- Droid moves first",
			"pvd":"(pvd) Player vs. Droid --- Player moves first"}
	self.gameType=self.set_gameType(self.gameTypes["dvd"])
	self.playerName=None

   def select_gameType(self):
	pass

   def set_gameType(self):

c= TicTacToe()
d= c.get_display()
print d
