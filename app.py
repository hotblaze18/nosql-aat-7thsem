from flask import Flask
from flask import render_template, request, redirect, url_for
import db
from bson.objectid import ObjectId
import json


app = Flask(__name__)
collection_name = "exports"

@app.route('/')
def home():
    data = db.exports.find().limit(100).sort("_id", -1)
    return render_template('main.html', data=data)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/add', methods = ['POST'])
def addExport():
    document = {}
    document['HSCode'] = request.form["hscode"]
    document['Commodity'] = request.form["commodity"]
    document['country'] = request.form["country"]
    document['value'] = request.form["value"]
    document['year'] = request.form["year"]
    db.exports.insert_one(document)
    data = db.exports.find().limit(100).sort("_id", -1)
    return render_template('main.html', message="Succesfully added new record", data=data)

@app.route('/update')
def update():
  id = request.args.get("id")
  data = db.exports.find_one({ '_id': ObjectId(id) })
  return render_template('update.html', data=data)

@app.route('/updateExport', methods = ['POST'])
def updateExport():
  id = request.form["id"]
  present_data= db.exports.find_one({ '_id': ObjectId(id) })
  document = {}
  document['HSCode'] = request.form["hscode"]
  document['Commodity'] = request.form["commodity"]
  document['country'] = request.form["country"]
  document['value'] = request.form["value"]
  document['year'] = request.form["year"]
  db.exports.update_one(present_data, { '$set': document })
  return redirect(url_for('home'))

@app.route('/delete', methods = ['POST'])
def delete():
  id = request.form["id"]
  db.exports.delete_one({'_id': ObjectId(id)})
  return redirect(url_for('home'))

@app.route('/visualize')
def visualize():
  data = db.exports.aggregate([
    {
      "$group" :
        {
          "_id" : "$country",
          "totalExports" : { "$sum": "$value" }
        }
     },
     {
       "$skip": 50
     },
     {
       "$limit": 30
     }
  ])
  countries = []
  exports = []
  for record in data:
    countries.append(record['_id'])
    exports.append(record['totalExports'])
  return render_template('visualize.html', countries=json.dumps(countries), exports=json.dumps(exports))

if __name__ == '__main__':
    app.run(port=8000)