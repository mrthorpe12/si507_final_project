from flask import Flask, redirect, url_for, render_template, request
from copy import deepcopy
import requests
import requests_cache
import time

from constants import AEROAPI_KEY, AEROAPI_BASE_URL, MAJOR_AIRPORT_DISTS, DETROIT_CODE_ICAO, DELTA_CODE_ICAO
from utils import open_cache, save_cache, build_cache

app = Flask(__name__)
requests_cache.install_cache(
    './database/flight_data_cache', backend='sqlite', expire_after=300)


class Airport():
    def __init__(self, name, code, city):
        self.name = name
        self.code = code
        self.city = city
        self.destinations = []


class FlightPlan():
    def __init__(self, legs, mileage):
        self.legs = legs
        self.mileage = mileage


@app.route('/', methods=['GET', 'POST'])
def home():
    airports = loadData(MAJOR_AIRPORT_DISTS)
    originCode = ""
    destCode = ""

    if request.method == "POST":
        originCode = request.form['origin']
        destCode = request.form['dest']

    print('Origin code: ', originCode)
    print('Destination code: ', destCode)

    userOrigin = getAirport(originCode, airports)
    userDest = getAirport(destCode, airports)

    print(f'Selected origin: {userOrigin}\nType: {type(userOrigin)}')
    print(f'Selected dest: {userDest}\nType: {type(userDest)}')

    shortestPlan = FlightPlan([], 0)
    findPath([FlightPlan([userOrigin], 0)], userDest, shortestPlan)

    return render_template('data.html', content=airports, path=shortestPlan)


def findPath(originList, dest, shortestPlan, searchedList=[]):
    for plan in originList:
        searchedList.append(plan.legs[-1])
    nextList = []
    for plan in originList:
        originAirport = plan.legs[-1]
        for childAirport, distance in originAirport.destinations:
            if childAirport not in searchedList:
                legsCopy = deepcopy(plan.legs)
                legsCopy.append(childAirport)
                childPlan = FlightPlan(
                    legs=legsCopy, mileage=plan.mileage+distance)
                if childAirport.name != dest.name:
                    nextList.append(childPlan)
                else:
                    if len(childPlan.legs) > 2:
                        if shortestPlan.mileage == 0 or childPlan.mileage < shortestPlan.mileage:
                            shortestPlan.legs = childPlan.legs
                            shortestPlan.mileage = childPlan.mileage
                        # print(childPlan.legs, childPlan.mileage)

    # print('Length of next list: ', len(nextList))
    if len(nextList) > 0:
        findPath(originList=nextList, dest=dest, shortestPlan=shortestPlan,
                 searchedList=searchedList)


def getAirport(code, airportDict):
    for airport in airportDict.values():
        if airport.code == code:
            return airport


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
        originName = data[0].strip('"')
        originCity = data[1].strip('"')
        originCode = data[2].strip('"')

        destName = data[3].strip('"')
        destCity = data[4].strip('"')
        destCode = data[5].strip('"')
        distance = float(data[-1].lstrip('"').rstrip('"\n'))

        if originName not in airportList.keys():
            airportList[originName] = Airport(
                originName, originCode, originCity)

        if destName not in airportList.keys():
            airportList[destName] = Airport(destName, destCode, destCity)

        target = airportList.get(originName)
        target.destinations.append((airportList.get(destName), distance))

    return airportList


if __name__ == "__main__":
    app.run(debug=True)
