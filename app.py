from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.json_util import dumps
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
import json
import datetime
import pytz


Client = MongoClient("mongodb://db:27017")
db = Client["SensorData"]
coll = db["Values"]

db_user = Client["user"]
coll_user = db_user["userdata"]

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route("/bruhnch", methods=["GET"])
def bruh():
    return "bruh"


@app.route("/", methods=["GET"])
def index():
    get_date = str(datetime.datetime.now(tz=pytz.timezone("Europe/Stockholm")).date())
    newest_entry = coll.find({"Date": get_date}).sort("Time", -1).limit(1)

    response = []
    for x in newest_entry:
        response.append(x)
    return render_template("index.html", date=get_date, newest=dumps(response),)


@app.route("/user/login", methods=["POST"])
def login():
    username = request.authorization["username"]
    password = request.authorization["password"]

    response = coll_user.find_one({"username": username})
    if response:
        if bcrypt.check_password_hash(response["password"], password):
            return "Login test successful"

        else:
            return jsonify("invalid password")
    else:
        return jsonify("invalid username")


@app.route("/user/register", methods=["POST"])
def testing():
    username = request.authorization["username"]
    password = bcrypt.generate_password_hash(request.authorization["password"]).decode(
        "utf-8"
    )
    coll_user.insert_one({"username": username, "password": password})
    return jsonify({"username": username, "passwordHash": password})


@app.route("/measurements", methods=["GET"])
def finding():
    date_ins = request.args["date"]
    if not date_ins:
        return jsonify("Need to add ?date=")
    collection = coll.find({"Date": date_ins}).sort("Time", -1)
    response = []
    for x in collection:
        response.append(x)
    return dumps(response)


@app.route("/measurements", methods=["POST"])
def inserting():
    username = request.authorization["username"]
    password = request.authorization["password"]

    if not any(username or password):
        return jsonify("This function is protected")

    response = coll_user.find_one({"username": username})

    if response:
        if bcrypt.check_password_hash(response["password"], password):
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
                    "Date": "2020-04-27",
                    "Time": str(dt_swe.time()),  # XD lam
                }
            )
            return jsonify("Test data sent!")
        else:
            return jsonify("invalid username or password")
    else:
        return jsonify("invalid username or password")


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
