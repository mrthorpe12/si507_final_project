from constants import AIRPORT_DISTS


class Airport():
    def __init__(self, name, code, city):
        self.name = name
        self.code = code
        self.city = city
        self.distances = []


def _findPath(origin, dest, count=0, searchedList=[], pathList=[]):
    for airport, distance in origin.distances:
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


def findPath(originList, dest, searchedList=[], pathList=[]):
    # loop through all airports in originList.distances
    nextList = []
    for airport in originList:
        for childAirport, distance in airport.distances:
            print(childAirport.name)
            if childAirport.name != dest.name and childAirport not in searchedList:
                nextList.append(childAirport)
            else:
                print('Found!')

            searchedList.append(childAirport)

    # print('Length of next list: ', len(nextList))
    if len(nextList) > 0:
        findPath(originList=nextList, dest=dest,
             searchedList=searchedList, pathList=pathList)


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
        target.distances.append((airportList.get(destName), distance))

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

    path = findPath(userOrigin, userDest[0])
    # print('Path: ', path)


if __name__ == "__main__":
    main()
