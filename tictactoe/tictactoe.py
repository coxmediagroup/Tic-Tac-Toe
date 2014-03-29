#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp import template

class MainPage (webapp2.RequestHandler):
    def get (self):
        self.response.out.write(template.render('views/tictactoe.html',{}))
        
    def post (self):
        self.get()

app = webapp2.WSGIApplication([
    webapp2.Route('/tictactoe', MainPage),
    ], debug=True)
