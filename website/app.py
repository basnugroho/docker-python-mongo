from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017") # db must be the same as the name in docker-compose.yml
db = client.aNewDB # create db
UserNum = db["UserNum"] # create collection
# insert doc
UserNum.insert({
    'num_of_users': 0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({}, {"$set":{"num_of_users": new_num}})
        return str("Hello user " + str(new_num))

def checkPostedData(postedData, functionName):
    if (functionName == "add"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
class Add(Resource):
    def post(self):
        # get posted data
        postedData = request.get_json()

        # verify validity
        status_code = checkPostedData(postedData, "add")
        if (status_code != 200):
            retJson = {
                'Message': "missing parameter",
                'Status Code': status_code
            }
            return jsonify(retJson)

        # if here then status_code = 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        # add the posted data
        ret = x + y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

    def get(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass

class Subsctract(Resource):
    def post(self):
        # get posted data
        postedData = request.get_json()

        # verify validity
        status_code = checkPostedData(postedData, "substract")
        if (status_code != 200):
            retJson = {
                'Message': "missing parameter",
                'Status Code': status_code
            }
            return jsonify(retJson)

        # if here then status_code = 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        # add the posted data
        ret = x + y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Multiply(Resource):
    pass

class Divide(Resource):
    pass

api.add_resource(Add,"/add")
api.add_resource(Visit,"/hello")

@app.route('/')
def hello_world():
    return "halo dunia!"

@app.route('/bye')
def bye():
    return "bye bye!"

if __name__== "__main__":
    app.run(host='0.0.0.0')
