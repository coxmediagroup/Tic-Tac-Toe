from django.db import models

# Create your models here.

class TicBoard(models.Model):

	nxo=(
                ('n', 'N'),
                ('x', 'X'),
                ('o','O'),
                )
	# I realize this violates the relational model and DRY 
	# however, clarity and simplicity sometimes trump normalization. 

	a=models.CharField(max_length=1, choices=nxo,default="n")
	b=models.CharField(max_length=1, choices=nxo,default="n")
	c=models.CharField(max_length=1, choices=nxo,default="n")
	d=models.CharField(max_length=1, choices=nxo,default="n")
	e=models.CharField(max_length=1, choices=nxo,default="n")
	f=models.CharField(max_length=1, choices=nxo,default="n")
	g=models.CharField(max_length=1, choices=nxo,default="n")
	h=models.CharField(max_length=1, choices=nxo,default="n")
	i=models.CharField(max_length=1, choices=nxo,default="n")

	
