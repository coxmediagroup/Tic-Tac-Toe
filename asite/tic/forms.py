from django.forms import ModelForm
from tic.models import TicBoard



class TicBoardForm(ModelForm):
	class Meta:
		model = TicBoard

	# use to check for winning moves and blocking moves

	def wingroups(self):
		return [	["a","e","i"],["c","e","g"],
				["d","e","f"],["b","e","h"],
				["a","b","c"],["g","h","i"],
				["a","d","g"],["c","f","i"]
			 ]

			  
	# If No win is possible and no block is needed,
		#This is the order in which the computer will pick 

	def xmoves(self):	
		
		return ["e","g","a","i","d","f","c","h","g","i"]


		# grabs values from request.Post for a wingroup

	def mkGrp(self,rp,grp):
		return [rp[k] for k in grp]	


		# looks for two 'x' or two 'o' values and one 'n' in a wingroup

	def chkCount(self,gvals,N,xo):
		if gvals.count(xo)== 2 and gvals.count(N)== 1:
			return True 

	
		# iterates wingroups for winning or blocking move.
		# and returns the 'pick' for x and the group
		#the group is used to mark winning moves.

	def chkGrps(self,rp,xo):
		N='n'
		for grp in self.wingroups():
			gvals=self.mkGrp(rp,grp)
			if self.chkCount(gvals,N,xo):
				pick =grp[gvals.index(N)]
				return pick,grp		
			else:
				pass		


		#if no winning move and no block move
		# find first open space in xmoves 

	def findOpen(self,rp,n):
		for xm in self.xmoves():
			if rp[xm]== n:
				return xm

	
		# returns a winning move, and winning group list 
		# or returns a block move and an empty list 
		# or returns next open move from xmoves	and a empty list

	def mkPick(self,rp):
		w=[]
		if self.chkGrps(rp,'x',):
			p,w=self.chkGrps(rp,'x')
			return p,w
	
		if self.chkGrps(rp,'o'):
			p,blah=self.chkGrps(rp,'o')	
			return p,w		
		else:
			p=self.findOpen(rp,'n')			
			return p,w

	
	
		
