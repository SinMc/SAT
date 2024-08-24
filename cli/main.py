"""
[changeme]
"""
import os
import requests
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

filepath = './cli/test/fixtures/test.csv'

def main(input_path):
    # pass
    response_json = network_request()
    with open("coordinate.json", "w") as file: 
         file.write(json.dumps(response_json))
    return ["coordinate.json"]


def format_output():
    with open("./coord.json", "r") as f:
        data = json.load(f)
    
    d = data["severities"]

    for rcp in d:
        # print(rcp)
        r = d[rcp]
        filtered = {k: v for k, v in r.items() if v !=None}
        r.clear()
        r.update(filtered)
        for hazard in r:
            # print(hazard)
            h = r[hazard]
            # print(h)
            for number in h:
                # print(number)
                n = h[number]
                x = n.keys()
                y = n.values()
                plt.plot(x,y)
    plt.savefig("graph.png")
                # print(n)
    # a = data["severities"]["rcp85"]["flood_riverine"]["500.0"]
    # x = a.keys()
    # y = a.values()
    # plt.plot(x, y)
    # plt.savefig("graph.png")
    # return ["graph.png"]



def retrieve_locations(filepath: str):
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()  # read the file

    locations = []

    for line in lines[1:]:
        separatedcoords = line.split(",") # separates the coordinate values
        lat = float(separatedcoords[0].strip())
        lon = float(separatedcoords[1].strip())
        n_coordinate = {"coordinates":{"latitude":lat,"longitude":lon}}
        locations.append(n_coordinate)
    return locations


def network_request():
    locations = retrieve_locations(filepath)
    url = "https://api.climaterisk.qa/v1/severities"
    api_token = os.environ.get("SEVERITIES_API_TOKEN")
    headers = {"Authorization": "Basic {}".format(api_token)}

    # print("\n\n $$$$$ \n\n")
    response_json = []
    for location in locations:
        response = requests.post(url, data= json.dumps(location), headers= headers)
        response_json.append(response.json())
    # print(response_json)
    return response_json
    # curl --request POST 
    # --url https://api.climaterisk.qa/v1/severities 
    # --header "Authorization: Basic $SEVERITIES_API_TOKEN" 
    # --data "{\"coordinates\":{\"latitude\":-32.92874606286358,\"longitude\":151.7829704479731}}"
    # --data '{"coordinates":{"latitude":-32.92874606286358,"longitude":151.7829704479731}}'


if __name__ == "__main__":
    # called when run from the command line

    if len(sys.argv) < 2:
        print("Please provide a filepath.")
        sys.exit(1)

    filepath = sys.argv[1]
    main(filepath)
