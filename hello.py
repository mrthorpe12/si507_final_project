from flask import Flask, redirect, url_for, render_template
import requests
import requests_cache
import time

from constants import AEROAPI_KEY, AEROAPI_BASE_URL, AIRPORT_DISTS, DETROIT_CODE_ICAO, DELTA_CODE_ICAO
from utils import open_cache, save_cache, build_cache

app = Flask(__name__)
requests_cache.install_cache(
    './database/flight_data_cache', backend='sqlite', expire_after=300)


class Airport():
    def __init__(self, name, code, city):
        self.name = name
        self.code = code
        self.city = city
        self.distances = []


@app.route('/')
def home():
    airports = loadData(AIRPORT_DISTS)
    # return "Hello, world!  This is the homepage."
    return render_template('data.html', content=airports)


def getData():
    # payload = {'max_pages': 2}
    auth_header = {'x-apikey': AEROAPI_KEY}
    # url = AEROAPI_BASE_URL + f"airports/{DETROIT_CODE_ICAO}/flights"
    url = AEROAPI_BASE_URL + f"operators/{DELTA_CODE_ICAO}/flights"

    # response = requests.get(url, params=payload, headers=auth_header)
    response = requests.get(url, headers=auth_header)
    now = time.ctime(int(time.time()))
    print(f"Time: {now}, Used Cache: {response.from_cache}")

    build_cache(response)

    if response.status_code == 200:
        return response.json()
    else:
        print('Error -- unable to execute request')


def loadData(file):
    airportList = {}
    document = open(file, "r")

    lines = document.readlines()

    for line in lines:
        data = line.split(',')
        originName = data[0]
        originCity = data[1]
        originCode = data[2]

        destName = data[3]
        destCity = data[4]
        destCode = data[5]
        distance = data[-1]

        if originName not in airportList.keys():
            airportList[originName] = Airport(
                originName, originCode, originCity)

        if destName not in airportList.keys():
            airportList[destName] = Airport(destName, destCode, destCity)

        target = airportList.get(originName)
        target.distances.append((airportList.get(destName), distance))

    return airportList


if __name__ == "__main__":
    app.run(debug=True)
