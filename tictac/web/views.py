from flask import request, session, render_template, abort, flash

from tictac.web import app

#
@app.route("/", methods=['GET'])
def index():
    return "Hello, world!"




