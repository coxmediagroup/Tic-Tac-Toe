from gevent import http
import json
import mimetypes
import os
from toebot import ToeBot

pwd = os.path.abspath(os.path.dirname(__file__))
bot = ToeBot()

def file_not_found(request):
    request.add_output_header('Content-Type', 'text/plain')
    request.send_reply(404, "NOT FOUND", '')

def handle_ajax(cmd, val):
    r = {}
    if cmd == 'reset':
        bot.reset()
        if val == "true":
            r['mymove'] = bot.my_move()
    elif cmd == 'human':
        bot.their_move(int(val))
        r = {}
        if bot.state == -1:
            r['mymove'] = bot.my_move()
            
    r['state'] = bot.state
    return r

def static_app(request):
    path = request.uri.strip('/')

    if not path:
        request.add_output_header('Content-Type', 'text/html')
        request.send_reply(200, "OK", open('static/index.html').read())

    elif path[0] == '?':
        cmd, val = path[1:].split('=')
        resp = handle_ajax(cmd, val)
        request.add_output_header('Content-Type', 'application/json')
        request.send_reply(200, "OK", json.dumps(resp))
    else:
        path = os.path.join(pwd, 'static', request.uri.strip('/'))

        if not os.path.exists(path):
            file_not_found(request)
        else:
            data = open(path).read()
            
            ct = mimetypes.guess_type(path)[0]
            
            request.add_output_header('Content-Type', ct or 'text/plain')
            request.send_reply(200, "OK", data)

if __name__=='__main__':
    print "Go to http://127.0.0.1:8000/"
    http.HTTPServer(('127.0.0.1', 8000), static_app).serve_forever()
