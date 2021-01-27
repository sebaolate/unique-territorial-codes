from bottle import Bottle ,redirect
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps

app = Bottle()
plugin = MongoPlugin(uri="mongodb://127.0.0.1", db="unique_territorial_db", json_mongo=True)
app.install(plugin)

@app.route('/regions', method='GET')
def index(mongodb):
    return dumps(mongodb['regions'].find())

@app.route('/provinces', method='GET')
def index(mongodb):
    return dumps(mongodb['provinces'].find())

@app.route('/communes', method='GET')
def index(mongodb):
    return dumps(mongodb['communes'].find())

app.run(host='localhost', port=8080)