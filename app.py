from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.json_util import dumps
import json
import datetime
import pytz


Client = MongoClient("Localhost", 27017)
db = Client["SensorData"]
coll = db["Values"]

app = Flask(__name__)


@app.route("/")
def index():
    get_date = datetime.datetime.now(tz=pytz.timezone("Europe/Stockholm")).date()
    newest_entry = coll.find({}).limit(1)

    return render_template("index.html", date=get_date, newest=newest_entry,)


@app.route("/testing", methods=["GET"])
def testing():
    x = request.authorization["username"]
    y = request.authorization["password"]

    if x == "Bruh" and y == "bru":

        return jsonify("u don complet it")
    else:
        return jsonify("u don gofed!")


@app.route("/measurements", methods=["GET"])
def finding():
    date_ins = request.args["date"]
    collection = coll.find({"Date": date_ins}).sort("Time", -1)
    response = []
    for x in collection:
        response.append(x)
    return dumps(response)


@app.route("/measurements", methods=["POST"])
def inserting():

    dt_swe = datetime.datetime.now(tz=pytz.timezone("Europe/Stockholm"))

    coll.insert_one(
        {
            "Temperature": request.json["Temp"],
            "Humidity": request.json["Hum"],
            "Pressure": request.json["Press"],
            "CO2": request.json["CO2"],
            "TVOC": request.json["TVOC"],
            "Rain": request.json["Rain"],
            "Wind": request.json["Wind"],
            "Date": str(dt_swe.date()),
            "Time": str(dt_swe.time()),
        }
    )
    return jsonify("OK")


@app.route("/measurements/user", methods=["GET"])
def user_finding():

    date_ins = request.args["date"]
    try_date = coll.count_documents({"Date": date_ins})
    if try_date == 0:
        return "<h3>No data found</h3>"

    else:
        collection = coll.find({"Date": date_ins}).sort("Time", -1)
        return render_template("user.html", coll=collection, date=date_ins)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=69)
