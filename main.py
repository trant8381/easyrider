import json
from collections import OrderedDict, Counter
from sys import exit
from datetime import datetime


def find(key_name, value_name, routes_list):
    for route in range(len(routes_list)):
        if routes_list[route][key_name] == value_name:
            return routes_list[route]
    return False


class Route:
    def __init__(self, start, final, stopp):
        self.start = start
        self.final = final
        self.stops = []

        index = "0"
        while True:
            if index == "0":
                self.stops += [find("stop_type", "S", stopp)]
            else:
                self.stops += [find("stop_id", index, stopp)]
                if self.stops[-1]["stop_type"] == "F":
                    break
            index = self.stops[-1]["next_stop"]

    def get_start(self):
        return self.start

    def get_final(self):
        return self.final

    def get_stops(self):
        return self.stops


if __name__ == "__main__":
    def amount_types(routes_list):
        starts = set()
        transfers = ""
        finals = set()
        for route in routes_list:
            starts.add(route.get_start()["stop_name"])
            transfers += "  ".join([i["stop_name"] for i in route.get_stops()]) + "  "
            finals.add(route.get_final()["stop_name"])
        transfers = sorted(list(filter(
            lambda x: x != 0,
            [k if v > 1 else 0 for k, v in dict(Counter(transfers.split("  "))).items()]
        )))
        return {"starts": starts, "transfers": transfers, "finals": finals}

    def print_routes(routes_list):
        results = amount_types(routes_list)
        print(f"Start stops: {len(results['starts'])} {sorted(list(results['starts']))}\n"
              f"Transfer stops: {len(results['transfers'])} {results['transfers']}\n"
              f"Finish stops: {len(results['finals'])} {sorted(list(results['finals']))}")
        
    def arrival_time_test(routes_list):
        print("Arrival time test:")
        fail = False
        for route in routes_list:
            stopps = route.get_stops()
            for stopp in range(len(stopps) - 1):
                if datetime.strptime(stopps[stopp]["a_time"], "%H:%M") > \
                        datetime.strptime(stopps[stopp + 1]["a_time"], "%H:%M"):
                    fail = True
                    print(f"bus_id line {stopps[stopp]['bus_id']}: "
                          f"wrong time on station {stopps[stopp + 1]['stop_name']}")
                    break
        if not fail:
            print("OK")

    def on_demand_test(routes_list, stopps):
        print("On demand stops test:")

        alt = [i for item in list(amount_types(routes_list).values()) for i in item]
        comp = []
        for stopp in stopps:
            if stopp["stop_type"] == "O":
                comp += [stopp["stop_name"]]

        contrast = []
        for item in comp:
            if item in alt:
                contrast += [item]

        print(f"Wrong stop type: {sorted(contrast)}" if len(contrast) > 0 else "OK")

    stops = json.loads(input())
    routes = OrderedDict()

    for stop in stops:
        if stop["bus_id"] in routes.keys():
            routes[stop["bus_id"]] += [stop]
        else:
            routes[stop["bus_id"]] = [stop]

    processed_routes = []
    for stop_id, stops_list in routes.items():
        s = find("stop_type", "S", stops_list)
        f = find("stop_type", "F", stops_list)
        if not s or not f:
            print(f"There is no start or end stop for the line: {stop_id}.")
            exit()
        else:
            processed_routes += [Route(s, f, stops_list)]

    on_demand_test(processed_routes, stops)