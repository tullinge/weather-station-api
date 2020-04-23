from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from requests import get
from bson.json_util import dumps
import json
import datetime
import socket
import pytz


Client = MongoClient("Localhost", 27017)
db = Client["SensorData"]
coll = db["Values"]

get_date = datetime.datetime.now(tz=pytz.timezone("Europe/Stockholm")).date()
# newest_entry = coll.find({}))

# print(newest_entry)
print(get_date)
