from flask import Flask, session
from flask.ext.session import Session

app = Flask(__name__)
app.secret_key = 'xyzzy'

#Config Parameters
SESSION_TYPE = 'filesystem'

#End Config Paramters

app.config.from_object(__name__)

Session(app)

from tictac.web import views
