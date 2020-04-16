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


@app.route("/measurements", methods=["GET"])
def finding():
    date_ins = request.args["date"]

    return render_template(
        "find.html",
        title="Mätvärden från " + date_ins,
        coll=coll.find({"Date": date_ins}).sort("Date", -1),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=69)
