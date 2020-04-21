from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from requests import get
import datetime
import socket
import pytz


Client = MongoClient("Localhost", 27017)
db = Client["SensorData"]
coll = db["Values"]

app = Flask(__name__)


@app.route("/")
def index():
    host_ip = socket.gethostbyname(socket.gethostname())
    network_ip = get("https://api.ipify.org").text
    get_date = datetime.datetime.now(tz=pytz.timezone("Europe/Stockholm"))

    return render_template(
        "index.html", host_ip=host_ip, ip=network_ip, date=get_date.date()
    )


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


@app.route("/measurements", methods=["GET"])
def finding():
    date_ins = request.args["date"]

    try_date = coll.count_documents({"Date": date_ins})
    if try_date == 0:
        get_date = str(
            datetime.datetime.now(tz=pytz.timezone("Europe/Stockholm")).date()
        )

        return (
            "<h3>No data found, measured data spreads across 2020-04-17 to "
            + get_date
            + " </h3>"
        )

    else:
        collection = coll.find({"Date": date_ins}).sort("Time", -1)
        return render_template("find.html", coll=collection, date=date_ins)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=69)
