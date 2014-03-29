#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp import template

import json
import random

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
    def move(self, emptySquares):
        # just pick a random empty square
        return(random.choice(emptySquares))

    def get (self):
        emptySquares= json.loads(self.request.get('empty_squares'));
        resp = self.move(emptySquares);
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
