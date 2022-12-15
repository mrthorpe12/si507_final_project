from constants import AIRPORT_DISTS
from copy import deepcopy


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


def _findPath(origin, dest, count=0, searchedList=[], pathList=[]):
    for airport, distance in origin.destinations:
        # print(airport.name, distance)
        if count == 0:
            if airport.name != dest.name and airport not in searchedList:
                searchedList.append(airport)
                pathList.append(airport)
                _findPath(origin=airport, dest=dest, count=count + 1,
                          searchedList=searchedList, pathList=pathList)
        else:
            if airport.name != dest.name and airport not in searchedList:
                searchedList.append(airport)
                pathList.append(airport)
                _findPath(origin=airport, dest=dest, count=count + 1,
                          searchedList=searchedList, pathList=pathList)
            else:
                searchedList.append(airport)
                pathList.append(airport)
                return pathList


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


def main():
    # airports = loadData(AIRPORT_DISTS)
    airports = loadData('test.csv')

    originName = input('Enter an airport name: ')
    destName = input('Enter another airport name: ')

    userOrigin = [airport for airport in airports.values()
                  if airport.name == originName]
    userDest = [airport for airport in airports.values()
                if airport.name == destName]

    print(f'User origin: {userOrigin[0]} is of type {type(userOrigin[0])}')
    print(f'User destination: {userDest[0]} is of type {type(userDest[0])}')

    # path = findPath(userOrigin, userDest[0])
    shortestPlan = FlightPlan([], 0)
    findPath([FlightPlan(userOrigin, 0)], userDest[0], shortestPlan)

    for leg in shortestPlan.legs:
        print('Leg: ', leg.name)


if __name__ == "__main__":
    main()
