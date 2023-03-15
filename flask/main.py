import os

import requests
from flask_cors import CORS

from flask import Flask

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
API_KEY = os.environ["API_KEY"]
BASE_URL = "https://api.openweathermap.org/data/2.5"
LAT = 63.09525
LNG = 21.61627
CITY = "Vaasa"


@app.route("/")
def hello():
    return "<p>Hello world</p>"


@app.route("/current")
def current():
    r = requests.get(
        f"{BASE_URL}/weather?&lat={LAT}&lon={LNG}&appid={API_KEY}&units=metric"
    )
    return r.json()
