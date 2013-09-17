'''
	Name: ai.py
	Author: Matthew Reinbold
	Purpose: Series of services for making Tic-Tac-Toe decisions
'''
import json

def echoGameState( state ):
	# simply returns a json representation of the passed gamestate
	return json.dumps( state )