from flask import Flask
from flask_pymongo import pymongo

CONNECTION_STRING = "mongodb+srv://pranav:nosqlaat@cluster0.kuhgo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('myFirstDatabase')
exports = pymongo.collection.Collection(db, 'exports')