'''
	Name: start.py
	Author: Matthew Reinbold
	Purpose: Sets up a simple wsgi web server to respond to
		requests, serves as rudimentary controller for game
		state changes requiring AI decision making
'''


# define global defaults - change port if default is already in use
myport = 8080
from string import Template
from wsgiref import util


# standard template for display
requestTemplate = Template("""
<html>
	<head><title>$title</title></head>
	<body>
		$body
	</body>
</html>
	""")

# define basic properties for various requests
requestInfo = {
	'home': {
		'title':"Welcome to Tic Tac Toe",
		'body':"<h1>This is a test of the temp templating system.</h1>"
	},
}


# handle requests is called when someone visits, builds output request
def handle_request( environment, start_response ):
	status = '200 OK' #HTTP status
	headers = [('Content-type',"text/html")]

	# determine the request intent from the path
	endPoint = environment["PATH_INFO"]
	
	# todo: for initial test, only returns the sample page
	if not endPoint == 'home':
		endPoint = 'home'

	start_response( status, headers )
	response = requestTemplate.substitute( **requestInfo[ endPoint ] )

	return [response]


# executed from the command line
if __name__ == '__main__':
	from wsgiref import simple_server

	print "Starting server on port " + str(myport) + "..."

	try:
		print "Now serving on port " + str(myport) + "!"
		print "[direct your browser to http://127.0.0.1:" + str(myport) + "]"
		httpd = simple_server.make_server('',myport,handle_request)
		httpd.serve_forever()
	except KeyboardInterrupt:
		print(" Ctrl-C detected. Server exiting.")
