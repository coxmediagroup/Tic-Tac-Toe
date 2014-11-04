from flask import Flask, request, session, g, render_template, abort, flash

app = Flask(__name__)
app.secret_key = 'xyzzy'


@app.route('/')
def index():
    return "Hello, world!"
