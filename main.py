from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS
import smtplib, ssl
import os
import sys
import urllib
import json
import random
import string
import time

app = Flask(__name__)  # Flask server
CORS(app)

client = MongoClient()  # Create client object

load_dotenv()  # Load environment variables

mongouri = "mongodb://" + urllib.parse.quote_plus(sys.argv[1]) + ":"\
        + urllib.parse.quote_plus(sys.argv[2]) + "@127.0.0.1:27017/"
client = MongoClient(mongouri)  # Client makes connection

db = client['ww-test']  # Select database

@app.route('/cars', methods=['GET'])
def sales():
    cars = db.cars.find()
    cars = json.loads(json_util.dumps(cars))
    for i in cars:
        i["_id"] = str(i["_id"]["$oid"])
    return cars


@app.route('/id', methods=['POST'])
def car_id():
    _id = request.get_json()
    id = _id["id"]
    car = db.cars.find_one({"_id": ObjectId(id)})
    car = json.loads(json_util.dumps(car))
    car["_id"] = str(car["_id"]["$oid"])
    return car

@app.route('/details_list', methods=['GET'])
def details_list():
    cars = db.cars.find()
    cars = json.loads(json_util.dumps(cars))

    make = []
    model = []
    year = []

    for doc in cars:
        make_value = doc['make']
        model_value = doc['model']
        year_value = doc['year']

        if make_value not in make:
            make.append(make_value)
        if model_value not in model:
            model.append(model_value)
        if year_value not in year:
            year.append(year_value)

    result = {'make': make, 'model': model, 'year': year}

    return jsonify(result)

@app.route('/find_car', methods=['POST'])
def find_car():
    details = request.get_json()
    make = details["make"]
    model = details["model"]
    year = details["year"]

    car = db.cars.find_one({"make": make, "model": model, "year": year})
    car = json.loads(json_util.dumps(car))
    car["_id"] = str(car["_id"]["$oid"])
    
    return car

if __name__ == '__main__':
    from waitress import serve
    # For local testing
    app.run(use_reloader=True, port=7000, threaded=True)
    # For deployment
    #tl.start()
    #serve(app, host="0.0.0.0", port=5000, url_scheme='https')
