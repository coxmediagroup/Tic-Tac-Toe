from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import argparse
import cgi
import os
import re
import threading
import urllib
import webbrowser
import ai

ip = '127.0.0.1'
port = '8052'
url = 'http://' + ip + ':' + port
port = int(port)
server = None

class html():
#class to scrape up some html out of the local files.

	def getHTML(self, sec):
		# Crack open those crazy html files and get the creamy goodness.
		path = os.path.dirname(os.path.abspath(__file__));
		url = 'file://' + path + '/' + str(sec) + '.html'
		sock = urllib.urlopen(url)
		htmlSource = sock.read()
		sock.close()
		return htmlSource

class RESTRequestHandler(BaseHTTPRequestHandler):
# This is the class that handles the RESTful requests.

	def do_HEAD(self):
	# This is just for checking the RESTful service.
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		return

	def do_GET(self):
	# This is the initial HTML generator. With this game, a GET request should only happen one time.
	# It's pretty much idempotent.
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		htmlcont = html()
		head = htmlcont.getHTML('head')
		body = htmlcont.getHTML('body')
		footer = htmlcont.getHTML('footer')
		print(self.wfile)
		self.wfile.write(head)
		self.wfile.write(body)
		self.wfile.write(footer)
		self.wfile.close()
		return

	def do_POST(self):  # This is for json formatted info
	# The POST verb will be used for most of the HTTP communications
		self.send_response(200)
		self.send_header('Content-Type', 'Application/json')
		self.end_headers()
		
		content_len = int(self.headers.getheader('content-length'))
		omatrix = self.rfile.read(content_len)
		# omatrix = '[{"1":2, "2":2, "3":1, "4":1, "5":2, "6":2, "7":2, "8":1, "9":1}]'
		comp = ai.comp()
		next_move = comp.next_move(omatrix) 
		ID = next_move

		print ID
		# print(self.wfile)
		self.wfile.write(ID)
		self.wfile.close()
		return

	def do_PUT(self):
	# Pretty much does nothing. It could be used to update a score or stats... maybe.
		return

	def do_DELETE(self):
	# This will quit the game by stopping the REST Service.
		global server
		server.stop()
		print 'Server Stopped!'
		return

# This is the meat of ther REST server.
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	allow_reuse_address = True

class SimpleHttpServer():
	def __init__(self, ip, port):
		self.server = ThreadedHTTPServer((ip,port), RESTRequestHandler)

	def start(self):
		self.server_thread = threading.Thread(target=self.server.serve_forever)
		self.server_thread.daemon = True
		self.server_thread.start()

	def waitForThread(self):
		self.server_thread.join()

	def stop(self):
		self.server.shutdown()
		self.waitForThread()

class LocalData(object):
# Not sure if this is completely necessary, but it's nice to give the data a place to live
	records = {}

class REST():
	def run(self):
		global server
		server = SimpleHttpServer(ip, port)
		print 'RESTful Server Running...........  Would you like to play a game?'
		server.start()
		webbrowser.open(url)
		server.waitForThread()