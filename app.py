from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from bson.json_util import dumps
from pymongo import MongoClient, ReturnDocument

import json

app = Flask(__name__)

api = Api(app)

mongoClient = MongoClient("mongodb://heroku_znmpshqc:4np638kram047ofq2miafp7hki@ds237770.mlab.com:37770/heroku_znmpshqc")
db = mongoClient["heroku_znmpshqc"]
user_collection = db.Youniverse

@app.route('/')
def index():
    return "Hello"

class User(Resource):
    def get(self, username):
        user = user_collection.find_one({"username":username})
        json_user = json.loads(dumps(user))
        return json_user

    def put(self, username):

        json_user = request.get_json()
        username_req = json_user["username"]
        user = user_collection.find_one({"username": username_req})

        updated_user = user_collection.insert_one({"username": username_req}, {"$set": json_user},
                                                                         return_document=ReturnDocument.AFTER)
        json_user_update = json.loads(dumps(updated_user))
        return json_user_update


api.add_resource(User, "/user/<username>")

if __name__ == '__main__':
    app.run()