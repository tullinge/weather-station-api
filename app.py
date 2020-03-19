from flask import Flask, request, jsonify

from pymongo import MongoClient
import datetime


Client = MongoClient("Localhost", 27017)
db = Client["val"]
coll = db["SensorData"]

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1> Home Page </h1>"


@app.route("/insert", methods=["POST", "GET"])
def inserting():

    coll.insert_one(
        {
            "temperature": request.json["temperature"],
            "Humidity": request.json["Humidity"],
            "Altitude": request.json["Altitude"],
            "Pressure": request.json["Pressure"],
            "CO2": request.json["CO2"],
            "TVOC": request.json["TVOC"],
            "Timestamp": datetime.datetime.utcnow(),
        }
    )
    return jsonify("Response")


@app.route("/test", methods=["POST", "GET"])
def testing():
    coll.insert_one({"temp": request.json["temp"]})
    return jsonify("Response")


if __name__ == "__main__":
    app.run(host="192.168.10.127", debug=True)

