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
	self.first_mover="X"
	self.second_mover="O"
	self.winners=([0,1,2], [3,4,5], [6,7,8], [0,4,8],
			[0,3,6], [1,4,7], [2,5,8], [2,4,6])
		
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

   def get_pairs(self):
   	pairs=[]
	for winner in self.winners:
	   pairs.append([winner[0], winner[1]])
	   pairs.append([winner[0], winner[2]])
	   pairs.append([winner[1], winner[2]])
	return pairs

   def get_superwinner(self, pair):
	for winner in self.winners:
	   if set(pair).issubset(winner):
	      return(winner)
	return [] 

   def get_potentialwinningpairs(self, state, matches):
	pwp=[]
	sw=None
	board=self.get_board()
	for pair in self.get_pairs():
	   if board[pair[0]] == state:
	      matches-=1
	   if board[pair[1]] == state:
	      matches-=1
           if matches <= 0:
	   	sw=self.get_superwinner()
		index=set(sw).difference(set(pair))
		if self.cell_is_mt(index):
		   pwp.append(pair)
	return pwp

   def get_potentialwinningmoves(self, state, matches):
        matchcount=matches
        moves=[]
        sw=None
        board=self.get_board()
        for pair in self.get_pairs():
	   matches=matchcount
           if board[pair[0]] == state:
              matches-=1
           if board[pair[1]] == state:
              matches-=1
           if matches <= 0:
                sw=self.get_superwinner(pair)
                index=set(sw).difference(set(pair)).pop()
                if self.cell_is_mt(index):
                   moves.append(index)
        return moves

   def get_blockingmove(self, state):
	if state=="X":
	   state="O"
	elif state=="O":
	   state="X"
	return self.get_winningmove(state)

   def get_winningmove(self, state):
        options = self.get_potentialwinningmoves(state,2)
        if len(options) > 0:
           return options[0]
        return None

   def get_appendingmove(self, state):
	options = self.get_potentialwinningmoves(state,1)
	if len(options) > 0:
	   return options[0]
	return None

   def get_centermove(self):
        centerindex=4
        index=None
        if (self.get_board()[centerindex]):
           index=centerindex
        return index

   def get_cornermove(self):
        cmoves=self.get_cornermoves()
        if len(cmoves) == 0:
           return None

	return cmoves[0]

   def get_cornermoves(self):
        board = self.get_board()
        corners=[0,2,6,8]
        moves=[]
        for corner in corners:
           if self.cell_is_mt(corner):
	      moves.append(corner)
        return moves 

   def reset_board(self):
	self.game_board=self.new_board()

   def set_player1(self, name):
	self.players[0]=name

   def set_player2(self, name):
	self.players[1]=name
  
   def set_players(self, nameList):
	self.set_player1(nameList[0])
	self.set_player2(nameList[1])

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
	   state=self.first_mover
	else:
	   state=self.second_mover
	return self.__set_cell__(cell_id, state)

   def set_lastmover(self):
	if self.last_mover==None or self.last_mover==1:
	   self.last_mover=0
	elif self.last_mover==0:
	   self.last_mover=1

   def get_firstmover(self):
	return self.first_mover
   
   def get_secondmover(self):
	return self.second_mover

   def get_lastmover(self):
	if self.last_mover==None:
	   return None
	return self.players[self.last_mover]

   def cell_is_mt(self, number):
	return self.game_board[number] == str(number)

   def get_Xmoves(self):

        counter=0

	xmoves= []
	for cellstate in self.game_board:
	   if cellstate=="X":
	      xmoves.append(counter)
	   counter+=1
	return xmoves

   def get_Omoves(self):

	counter=0

	omoves= []
	for cellstate in self.game_board:
	   if cellstate=="O":
	      omoves.append(counter)
	   counter+=1
	return omoves

   def get_moves(self):
	moves = self.get_Xmoves() + self.get_Omoves()
	moves.sort()
	return moves 

   def get_movecount(self):
        return len(self.get_moves())

   def get_emptycells(self):
	return set([0,1,2,3,4,5,6,7,8]).difference(self.get_moves())

   def get_opencorners(self):
	corners=set([0,2,6,8])
	return corners.intersection(self.get_emptycells())

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

   def hasa_winner(self):
	return self.get_winner() is not None

class TicTacToeController(object):
   def __init__(self, tictactoe):
	self.game=tictactoe
	#self.game=TicTacToe()
	self.droid1_skill="high" #"low", "medium", or "high"
	self.droid2_skill="low" #"low", "medium", or "high"
	self.droid_predictability="high" #"low", "medium", or "high"
	self.gameTypes={"dvd":"(1) Droid1 vs. Droid2",
			"dvp":"(2) Droid vs. Player --- Droid moves first",
			"pvd":"(3) Player vs. Droid --- Player moves first",
			"pvp":"(4) Player1 vs. Player2"}
	self.gameTypeToPlayers={"dvd":("Droid1", "Droid2"),
				"dvp":("Droid", "Player"),
				"pvd":("Player", "Droid"),
				"pvp":("Player1", "Player2")
				}
	self.gameType=None

   def play(self):
	play=True
	while play:
	   ##Get User Input For Game Type to Play or to Exit(play=False)
           m=self.gameTypes
           exit_option="(5) Exit"
	   choice = raw_input("Please select an option:\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t\t" %
				(m["dvd"],m["dvp"],m["pvd"],m["pvp"],exit_option))[0]
           if choice not in ["1", "2", "3", "4"]:
              play=False

	   if play:
                callMap={"1":self.play_dvd,
			"2":self.play_dvp,
			"3":self.play_pvd,
			"4":self.play_pvp}
	   	##Play the selected game type
                callMap[choice]()
	   self.game.reset_all()
	   #play=False

   def play_game(self, choice, gen1, gen2):
        self.gameType=self.gameTypes[choice]
        self.game.set_players(self.gameTypeToPlayers[choice])

        droid1=gen1()
        droid2=gen2()

        print self.game.get_display()
        count=0
        while not self.game.hasa_winner() and (len(self.game.get_emptycells()) > 0) and (count < 10):
                d1move=droid1.next()
                self.game.move(d1move)
                count+=1
		print self.game.get_display()
                if (not self.game.hasa_winner()) and (len(self.game.get_emptycells()) >0):
                        d2move=droid2.next()
                        self.game.move(d2move)
                        count+=1
                	print self.game.get_display()

   def play_dvd(self):
	self.play_game("dvd", self.smart_generator_X, self.good_generator_O)

   def play_dvp(self):
	self.play_game("dvp", self.smart_generator_X, self.manual_generator_O)

   def play_pvd(self):
	self.play_game("pvd", self.manual_generator_X, self.good_generator_O)

   def play_pvp(self):
	self.play_game("pvp", self.manual_generator_X, self.manual_generator_O)

   def select_gameType(self):
	pass

   def set_gameType(self, selection):
      if self.gameTypes.has_key(selection):
         self.gameType=self.gameTypes[selection]
         return True
      return False

   def center_move(self):
      index=self.game.get_centermove()
      if index != None:
         self.game.move(index)
         return True
      return False

   def corner_move(self):
      index=self.game.get_cornermove()
      if index != None:
         self.game.move(index)
	 return True
      return False

   def good_move(self, state):

      move_count=self.game.get_movecount()


      #Win if you can
      move=self.game.get_winningmove(state)

      #Block your competitors potential winning move
      if move==None: 
         move=self.game.get_blockingmove(state)
      else:
         return move

      #Create a potential winner
      if move==None: 
         move=self.game.get_appendingmove(state)
      else:
         return move

      #Make a corner move if it is safe to do so 
      if (move==None):
         if move_count == 0:
            move=self.game.get_cornermove()
      else:
         return move

      #Make a defensive move
      if move==None:
         move=self.game.get_centermove()
      else:
         return move

      #Make a corner move
      if move==None:
         move=self.game.get_cornermove()

      return move

	
   def smart_generator_X(self):
      #mover = self.game.get_firstmover() #simplify for now, assume X moves first
      while True:
         xmoves = self.game.get_Xmoves()
         omoves = self.game.get_Omoves()
         move_count = len(xmoves) + len(omoves)

         move=None
         if (move_count % 2) > 0:
	    #Error, it is not the first players move
            move=None
         elif (move_count == 0):
            #yield self.game.get_cornermove() ##keep simple, for now
            move=0
         elif (move_count == 2):
            if len( set(omoves).intersection( set([1,2]) ) ) == 0:
               move=2 
            elif len( set(omoves).intersection( set([3,6]) ) ) == 0:
               move=6
         elif (move_count >= 4):
            move=self.good_move("X") #assumed that first player uses X

         yield move

   def easy_generator(self):
      while True:
         yield int(self.game.get_emptycells().pop()) 

   def good_generator_XO(self, state="O"):
      while True:
         move = self.good_move(state)
         yield move 

   def good_generator_O(self):
      while True:
         move = self.good_move("O")
         yield move

   def manual_generator_X(self):
      while True:
         try:
            choice=int(raw_input("\nPlayer X: ")[0])
            yield choice
         except:
            pass

   def manual_generator_O(self):
      while True:
         try:
            choice=int(raw_input("\nPlayer O: ")[0])
            yield choice
         except:
            pass

def main():
  ttt=TicTacToe()
  control=TicTacToeController(ttt) 
  control.play()

if __name__ == "__main__":
   main()
