#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp import template

import json
import random

import pprint
pp = pprint.PrettyPrinter(indent=4)

#
# main page: start the first game and wait for the human to move
#
class MainPage (webapp2.RequestHandler):
    def get (self):
        self.response.out.write(template.render('views/tictactoe.html',{}))
        
    def post (self):
        self.get()

#
# pick server's next move
#
class Move (webapp2.RequestHandler):
    def move(self, emptySquares, winningScores, humanScore):
        # block human from any next-move win
        for i in emptySquares:
            # use the same algorithm applied by javascript to check for a win 
            for score in winningScores:
                if ( int(emptySquares[i]) + int(humanScore) & int(score) == int(score)):
                    return(i)
        # todo: thwart human for setting up a win
        # just pick a random empty square
        return(random.choice([i for i in emptySquares]))
            

    def get (self):
        parms = json.loads(self.request.get('parms'))
        emptySquares = parms['empty_squares']
        winningScores = parms['winning_scores']
        humanScore = parms['human_score']
        resp = self.move(emptySquares,winningScores,humanScore);
        self.response.out.write(resp)
        
    def post (self):
        self.get()

#
# route url to handler class
#
app = webapp2.WSGIApplication([
    webapp2.Route('/tictactoe', MainPage),
    webapp2.Route('/tictactoe/move', Move),
    ], debug=True)
