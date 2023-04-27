import os

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

API_KEY = os.environ["API_KEY"]
BASE_URL = "https://api.openweathermap.org/data/2.5"
LAT = 60.192059
LNG = 24.945831


@app.route("/", methods=["POST"])
def handle_post_request():
    return "Received POST request"


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
    try:
        r = requests.get(
            f"{BASE_URL}/weather?&lat={LAT}&lon={LNG}&appid={API_KEY}&units=metric"
        )
        r.raise_for_status()  # raise an error for non-2xx response codes
        response = r.json()
        icon = response["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/w/{icon}.png"
        icon = {"icon": icon_url}
        response.update(icon)
        return response
    except requests.exceptions.HTTPError as e:
        # handle HTTP errors
        return f"An HTTP error occurred: {e}"
    except requests.exceptions.RequestException as e:
        # handle other request errors
        return f"A request error occurred: {e}"


@app.route("/forecast")
def forecast():
    response = requests.get(
        f"{BASE_URL}/forecast?lat={LAT}&lon={LNG}&appid={API_KEY}&units=metric"
    )
    data = response.json()

    temps = []

    for forecast in data["list"]:
        temp = forecast["main"]
        weather = forecast["weather"]
        wind = forecast["wind"]
        dt = forecast["dt_txt"]
        temps.append(
            {
                "dt": dt,
                "feels_like": temp["feels_like"],
                "grnd_level": temp["grnd_level"],
                "humidity": temp["humidity"],
                "pressure": temp["pressure"],
                "sea_level": temp["sea_level"],
                "temp": temp["temp"],
                "temp_kf": temp["temp_kf"],
                "temp_max": temp["temp_max"],
                "temp_min": temp["temp_min"],
                "weather": weather,
                "wind": wind,
            }
        )

    return temps


@app.route("/reset")
def reset():
    global LAT, LNG
    LAT = 60.192059
    LNG = 24.945831
    return "Server reset"
