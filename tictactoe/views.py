# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.http import HttpResponse
from ticTacToe import TicTacToeEngine as game
from ticTacToe import TicTacToeCPU as CPU




def home(request):
	data = {}
	return render_to_response('tictactoe/index.html', data)
	
def begin_board(request):
	import random
	begins = random.randrange(0,2)
	if begins == 0:
		begins = "you"
	else:
		begins = "cpu"
	yours = random.randrange(0,2)
	if yours == 0:
		yours = "X"
		cpu = "O"
	else:
		yours = "O"
		cpu = "X"
	import datetime
	today = datetime.datetime.now()
	time = today.strftime("%d/%m/%y %H:%M:%S")
	log = "You are %s and CPU is %s" % (yours , cpu)
	if begins == "you":
		log = "%s, %s begin" % (log , begins)
	else:
		log = "%s, %s begins" % (log , begins)
	data = {
		"cpu"		:	cpu ,
		"yours"		:	yours ,
		"begins"	:	begins ,
		"board"		:	"NNNNNNNNN" ,
		"time" : time ,
		"moves" : "BEGINS" ,
		"log" : log ,
	}
	data = simplejson.dumps(data)
	return HttpResponse(data, mimetype='application/json')
	
def post_cpu_move(request):
	if request.method == 'GET':
		x = None
		y = None
		board = request.GET['board'] or None
		piece = request.GET['piece'] or None
		opp_peace = None
		if piece:
			if piece == "X":
				piece = "O"
				opp_peace = "X"
			else:
				piece = "X"
				opp_peace = "O"
		last_move = request.GET['last_move'] or None
		if last_move == "None":
			last_move = None
		last_x = request.GET['last_x'] or None
		if last_x == "None":
			last_x = None
		last_y = request.GET['last_y'] or None
		if last_y == "None":
			last_y = None
		last = {
			'value'	:	last_move ,
			'x'		: 	last_x ,
			'y'		:	last_y ,
		}

		try:
			engine = game()
			engine.setBoard(board)
			engine.setLast(last)
			cpu = CPU(current = engine.current , moves = engine.moves , cpu_peace = piece , opp_peace = opp_peace)
			x , y = cpu.getMove()
			engine.move(piece , x , y)
			board = engine.getBoard()
			last_move = engine.last['value']
			last_x = engine.last['x']
			last_y = engine.last['y']
			import datetime
			today = datetime.datetime.now()
			time = today.strftime("%d/%m/%y %H:%M:%S")
			data = {
				"board" : board ,
				"last_move" : last_move ,
				"last_x" : last_x ,
				"last_y" : last_y ,
				"moves" : engine.moves ,
				"log" : engine.getLog() ,
				"time" : time ,
				"won" : "0" ,
				"draw" : "0" ,
			}
		except Exception , e:
			if e.message == "WON":
				board = engine.getBoard()
				last_move = engine.last['value']
				last_x = engine.last['x']
				last_y = engine.last['y']
				import datetime
				today = datetime.datetime.now()
				time = today.strftime("%d/%m/%y %H:%M:%S")
				data = {
					"board" : board ,
					"last_move" : last_move ,
					"last_x" : last_x ,
					"last_y" : last_y ,
					"moves" : engine.moves ,
					"log" : engine.getLog() ,
					"time" : time ,
					"won" : "1" ,
					"draw" : "0" ,
				}
			elif e.message == "DRAW":
				board = engine.getBoard()
				last_move = engine.last['value']
				last_x = engine.last['x']
				last_y = engine.last['y']
				import datetime
				today = datetime.datetime.now()
				time = today.strftime("%d/%m/%y %H:%M:%S")
				data = {
					"board" : board ,
					"last_move" : last_move ,
					"last_x" : last_x ,
					"last_y" : last_y ,
					"moves" : engine.moves ,
					"log" : engine.getLog() ,
					"time" : time ,
					"won" : "0" ,
					"draw" : "1" ,
				}
			else:
				data = {
					"msg" : e.message ,
					"error" : "1",
				}
	elif request.method == 'POST':
		data = {
			"msg" : "unknow error" ,
			"error" : "1",
		}
	data = simplejson.dumps(data)
	return HttpResponse(data, mimetype='application/json')

def post_your_move(request):
	if request.method == 'GET':
		x = request.GET['x'] or None
		y = request.GET['y'] or None
		board = request.GET['board'] or None
		piece = request.GET['piece'] or None
		last_move = request.GET['last_move'] or None
		if last_move == "None":
			last_move = None
		last_x = request.GET['last_x'] or None
		if last_x == "None":
			last_x = None
		last_y = request.GET['last_y'] or None
		if last_y == "None":
			last_y = None
		last = {
			'value'	:	last_move ,
			'x'		: 	last_x ,
			'y'		:	last_y ,
		}
		try:
			engine = game()
			engine.setBoard(board)
			engine.setLast(last)
			engine.move(piece , x , y)
			board = engine.getBoard()
			last_move = engine.last['value']
			last_x = engine.last['x']
			last_y = engine.last['y']
			import datetime
			today = datetime.datetime.now()
			time = today.strftime("%d/%m/%y %H:%M:%S")
			data = {
				"board" : board ,
				"last_move" : last_move ,
				"last_x" : last_x ,
				"last_y" : last_y ,
				"moves" : engine.moves ,
				"log" : engine.getLog() ,
				"time" : time ,
				"won" : "0" ,
				"draw" : "0" ,
			}
		except Exception , e:
			if e.message == "WON":
				board = engine.getBoard()
				last_move = engine.last['value']
				last_x = engine.last['x']
				last_y = engine.last['y']
				import datetime
				today = datetime.datetime.now()
				time = today.strftime("%d/%m/%y %H:%M:%S")
				data = {
					"board" : board ,
					"last_move" : last_move ,
					"last_x" : last_x ,
					"last_y" : last_y ,
					"moves" : engine.moves ,
					"log" : engine.getLog() ,
					"time" : time ,
					"won" : "1" ,
					"draw" : "0" ,
				}
			elif e.message == "DRAW":
				board = engine.getBoard()
				last_move = engine.last['value']
				last_x = engine.last['x']
				last_y = engine.last['y']
				import datetime
				today = datetime.datetime.now()
				time = today.strftime("%d/%m/%y %H:%M:%S")
				data = {
					"board" : board ,
					"last_move" : last_move ,
					"last_x" : last_x ,
					"last_y" : last_y ,
					"moves" : engine.moves ,
					"log" : engine.getLog() ,
					"time" : time ,
					"won" : "0" ,
					"draw" : "1" ,
				}
			else:
				data = {
					"msg" : e.message ,
					"error" : "1",
				}
	elif request.method == 'POST':
		data = {
			"msg" : "unknow error" ,
			"error" : "1",
		}
	data = simplejson.dumps(data)
	return HttpResponse(data, mimetype='application/json')