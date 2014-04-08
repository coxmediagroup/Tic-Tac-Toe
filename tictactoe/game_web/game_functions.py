
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import json

# Class for holding ordered pairs
# Will make code in checkWin cleaner
class CenterWinOrderedPair:

	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2


# Check to see if the last player that took a turn won the game
def checkWin(request):
	if request.POST:
		""" Static set of possible wins if the center was occupied
			by the last player that had a turn """
		centerWins = [
			CenterWinOrderedPair(0,0,2,2),
			CenterWinOrderedPair(1,0,1,2),
			CenterWinOrderedPair(2,0,0,2),
			CenterWinOrderedPair(2,1,0,1)
		]
		# Parse the json from the request
		board = json.loads(request.POST['board'])
		lastSpaceTaken = json.loads(request.POST['lastSpaceTaken'])

		""" Check which player took the last turn by checking
			the character located on the board at the coordinates
			of lastSpactTaken """
		lastPlayer = board[lastSpaceTaken[0]][lastSpaceTaken[1]]

		win = False
		""" Keep track of the coordinates checked so if a winning set of
			coordinates is found, we can display the winning spot to the user """
		winningSpots = [];

		# Check if the last player that played occupied the board's center
		if board[1][1] == lastPlayer:
			""" Check each ordered pair to see if the last player occupies
				both spots in each pair (since he/she already has the center) """
			for pair in centerWins:
				x1 = pair.x1
				y1 = pair.y1
				x2 = pair.x2
				y2 = pair.y2
				if board[x1][y1] == lastPlayer and board[x2][y2] == lastPlayer:
					win = True
					# Add the center to winning spots
					winningSpots.append([1,1])
					winningSpots.append([x1, y1])
					winningSpots.append([x2, y2])
					break
		# If the player is not declared the winner, check any other win possibilities
		if not win:
			""" First, check if the player won horizonally accoring to the lastSpaceTaken
				If we count three occurrences of the same character, the last player won """
			lastPlayerCount = 0
			# Make our conditional statements in the loop shorter
			# lstX is "lastSpaceTaken x coordinate"
			lstX = lastSpaceTaken[0]
			lstY = lastSpaceTaken[1]
			winningSpots = []
			for i in range(0,3):
				""" Use mod in for (x+1)%3 because that will cover all horizontal coordinates
					even if the lastSpaceTaken is in the center (e.g. of the bottom row)"""
				if board[lstX][(lstY+i)%3] == lastPlayer:
					lastPlayerCount+=1
				winningSpots.append([lstX,i])
			if lastPlayerCount == 3:
				win = True
			else:
				""" If the player still hasn't won, check if he/she won vertically using the
					same logic as above """
				lastPlayerCount = 0
				winningSpots = []
				for j in range(0,3):
					if board[(lstX+j)%3][lstY] == lastPlayer:
						lastPlayerCount+=1
					winningSpots.append([j,lstY])
				if lastPlayerCount == 3:
					win = True
		# Convert our variables into JSON and respond to the AJAX request
		results = {
			'win': win,
			'winningSpots': winningSpots
		}
		json_results = json.dumps(results)
		return HttpResponse(json_results, mimetype="application/json")

def AI_turn(request):
	pass