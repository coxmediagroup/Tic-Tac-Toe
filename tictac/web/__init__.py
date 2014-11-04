from flask import Flask

app = Flask(__name__)
app.secret_key = 'xyzzy'

from tictac.web import views

