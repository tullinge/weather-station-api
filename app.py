from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from requests import get
import datetime
import socket


Client = MongoClient("Localhost", 27017)
db = Client["val"]
coll = db["SensorData"]

app = Flask(__name__)


@app.route("/")
def index():
    host_ip = socket.gethostbyname(socket.gethostname())
    network_ip = get("https://api.ipify.org").text
    return render_template("index.html", host_ip=host_ip, ip=network_ip)


@app.route("/measurements", methods=["POST"])
def inserting():

    date_init = datetime.datetime.utcnow()
    date_subt = datetime.timedelta(hours=1)
    date_ins = date_init + date_subt

    coll.insert_one(
        {
            "Temperature": request.json["Temp"],
            "Humidity": request.json["Hum"],
            # "Altitude": request.json["Alt"]
            "Pressure": request.json["Press"],
            "CO2": request.json["CO2"],
            "TVOC": request.json["TVOC"],
            "Rain": request.json["Rain"],
            "Wind": request.json["Wind"],
            "Date": str(date_ins.date()),
            "Time": str(date_ins.time()),
        }
    )
    return jsonify("OK")


@app.route("/test", methods=["POST"])
def testing():
    date_init = datetime.datetime.utcnow()
    date_subt = datetime.timedelta(hours=1)
    date_ins = date_init + date_subt
    coll.insert_one(
        {
            "Temp": request.json["temp"],
            "Date": str(date_ins.date()),
            "Time": str(date_ins.time()),
        }
    )
    return jsonify("Response")


@app.route("/find", methods=["GET"])
def finding():
    date_ins = request.args["date"]
    output = []

    for joe in coll.find({"Date": date_ins}).sort("Date", -1):
        output.append(joe)

    return render_template("find.html", title="Sensor DB list", paragraph=output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=69)
