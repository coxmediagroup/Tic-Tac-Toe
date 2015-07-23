from flask import Flask
from flask.ext.pymongo import PyMongo
app   = Flask(__name__)
app.config['MONGO_DBNAME'] = 'joshua'
mongo = PyMongo(app)


@app.route("/")
def hello():
    #result   = mongo.db.results.insert({'type':'total','0':0,'1':0,'2':0})
    return "Greetings Professor Falcon"


@app.route('/winner/<thewinner>')
def upload_winner(thewinner):
    # show the user profile for that user
    themap  = {'o':'0', 'x':'1', '0':'2'}
    result1   = mongo.db.results.find_one_or_404({'type':'total'})
    current   = result1[themap[thewinner]]
    newvalue  = int(current) + 1
    result1[themap[thewinner]] = newvalue
    result2                    = mongo.db.results.update({'type':'total'},result1)
    return '{"winner":"%s"}' % newvalue

@app.route('/results')
def download_record():
    # show the user profile for that user
    result1   = mongo.db.results.find_one_or_404({'type':'total'})
    return '{"total":[%s,%s,%s]}' % ( result1['0'], result1['1'], result1['2'])


if __name__ == "__main__":
    app.run()