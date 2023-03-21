import os

import requests
from flask_cors import CORS

from flask import Flask, request

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

API_KEY = os.environ["API_KEY"]
BASE_URL = "https://api.openweathermap.org/data/2.5"
LAT = 60.192059
LNG = 24.945831


@app.route("/api/location", methods=["POST"])
def receive_location():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    global LAT, LNG
    LAT = latitude
    LNG = longitude
    return "Location received"


@app.route("/current")
def current():
    r = requests.get(
        f"{BASE_URL}/weather?&lat={LAT}&lon={LNG}&appid={API_KEY}&units=metric"
    )
    response = r.json()
    icon = response["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/w/{icon}.png"
    icon = {"icon": icon_url}
    response.update(icon)

    return response


@app.route("/forecast")
def forecast():
    r = requests.get(
        f"{BASE_URL}/forecast?lat={LAT}&lon={LNG}&appid={API_KEY}&units=metric"
    )
    return r.json()
