from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import session
from flask import jsonify

from ticktacktoeai import AI

app = Flask(__name__)

#note: computer always starts off in top right corner. 
# should this be random? Not sure. 
DEFAULT_GAME_STATE = [
    -1,0,0,
    0,0,0,
    0,0,0
]

@app.route("/")
def home():
    session["state"] = list(DEFAULT_GAME_STATE)
    return render_template(
        'index.html'
    )
    
    
@app.route("/move", methods=['POST'])
def move():
    move = request.form['position']
    print "move: ", move
    
    try:
        move_data = session["state"][int(move)]
        if move_data != 0:
            raise Exception("invalid move")
            
        # mark players move if it is valid:
        session["state"][int(move)] = 1
        ai = AI.TickTackToeAI()

        cpmove = ai.getComputerMove( session["state"] )
        session["state"][ cpmove ] = -1
        
        return str(cpmove)
    except Exception, e:
        print "server error, ", e
        return "server error, ", e
    

@app.route("/clear", methods=['POST'])
def clear():
    session["state"] = list(DEFAULT_GAME_STATE)
    return "ok"
    

@app.route("/testai")
def testai():
    session["state"] = list(DEFAULT_GAME_STATE)
    
    # do something here to test the AI to make sure it always wins.
    
    return "ok"

    
if __name__ == "__main__":
    app.debug = True
    app.secret_key = "dfndsfunr4r8743q98rsrkq0llaqmsrajf"
    app.run()
    
    