import json


class Airport():
    def __init__(self, name, code, city):
        self.name = name
        self.code = code
        self.city = city
        self.destinations = []


def importGraphJson():
    file = open('./graph.json', 'r')
    fc = file.read()
    file_dict = json.loads(fc)
    file.close()

    airportDict = {}

    for key, value in file_dict.items():
        # print(key, value)
        airportDict[key] = Airport(value['name'], value['code'], value['city'])

    for key, value in file_dict.items():
        for airportName, mileage in value['destinations'].items():
            # print(airportName, mileage)
            airportDict[key].destinations.append(
                (airportDict.get(airportName), mileage))

    return airportDict


def main():
    graph = importGraphJson()
    print(graph)


if __name__ == "__main__":
    main()
