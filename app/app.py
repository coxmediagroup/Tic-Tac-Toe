from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import session
from flask import jsonify

import random

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
    cp_wins = 0
    user_wins = 0
    ties = 0
    ai = AI.TickTackToeAI()
    for game in range(1000):
        game_on = True
        session["state"] = list(DEFAULT_GAME_STATE)
        while game_on:
            if 0 not in session["state"]:
                game_on = False
                ties += 1
                break
                
            picking_user_move = True
            user_move = -1
            while picking_user_move and 0 in session["state"]:
                test = random.randrange(0,9)
                if session["state"][ test ] == 0:
                    user_move = test
                    picking_user_move = False
            
            session["state"][ user_move ] = 1
            user_win = ai.didPlayerWin( session["state"], True )
            if user_win != None:
                game_on = False
                user_wins += 1
                break
            
            cp_move = ai.getComputerMove( session["state"] )
            session["state"][ cp_move ] = -1        
            cp_win = ai.didPlayerWin( session["state"], False )
            if cp_win != None:
                game_on = False
                cp_wins += 1
                break
            
    winsdict = {}
    winsdict["computer_wins"] = cp_wins
    winsdict["user_wins"] = user_wins
    winsdict["ties"] = ties
    winsdict["total_runs"] = 1000
    return jsonify( winsdict )

    
if __name__ == "__main__":
    app.debug = True
    app.secret_key = "dfndsfunr4r8743q98rsrkq0llaqmsrajf"
    app.run()
    
    