from django.db import models

class Board(models.Model):

	nxo=(
                ('n', 'N'),
                ('x', 'X'),
                ('o','O'),
                )
	# I realize this violates the relational model and DRY 
	# however, clarity and simplicity sometimes trump normalization. 

	zero=models.CharField(max_length=1, choices=nxo,default="n")
	one=models.CharField(max_length=1, choices=nxo,default="n")
	two=models.CharField(max_length=1, choices=nxo,default="n")
	three=models.CharField(max_length=1, choices=nxo,default="n")
	four=models.CharField(max_length=1, choices=nxo,default="n")
	five=models.CharField(max_length=1, choices=nxo,default="n")
	six=models.CharField(max_length=1, choices=nxo,default="n")
	seven=models.CharField(max_length=1, choices=nxo,default="n")
	eight=models.CharField(max_length=1, choices=nxo,default="n")
	
	
	def __str__(self):

		return '%d'%self.id
        
	

	
	wingroups= [	["zero","four","eight"],["two","four","six"],["three","four","five"],
		["one","four","seven"],["zero","one","two"],["six","seven","eight"],
		["zero","three","six"],["two","five","eight"]	]

			  
	# If No win is possible and no block is needed,
		#This is the order in which the computer will pick 

	xmoves=["four","six","zero","eight","three","five","two","seven","six","eight"]
		
		

		# grabs values from request.Post for a wingroup

	def mkGrp(self,mtd,grp):
		return [mtd[k] for k in grp]	


		# looks for two 'x' or two 'o' values and one 'n' in a wingroup

	def chkCount(self,gvals,N,xo):
		if gvals.count(xo)== 2 and gvals.count(N)== 1:
			return True 

	
		# iterates wingroups for winning or blocking move.
		# and returns the 'pick' for x and the group
		#the group is used to mark winning moves.

	def chkGrps(self,mtd,xo):
		N='n'
		for grp in self.wingroups:
			gvals=self.mkGrp(mtd,grp)
			if self.chkCount(gvals,N,xo):
				pick =grp[gvals.index(N)]
				return pick,grp		
			else:
				pass		
	

	
		#if no winning move and no block move
		# find first open space in xmoves 

	def findOpen(self,mtd,n):
		for xm in self.xmoves:
			if mtd[xm]== n:
				return xm

	
		# returns a winning move, and winning group list 
		# or returns a block move and an empty list 
		# or returns next open move from xmoves	and a empty list

	def mkPick(self,mtd):
		w=[]
		if self.chkGrps(mtd,'x',):
			p,w=self.chkGrps(mtd,'x')
			return p,w
	
		if self.chkGrps(mtd,'o'):
			p,blah=self.chkGrps(mtd,'o')	
			return p,w		
		else:
			p=self.findOpen(mtd,'n')			
			return p,w
