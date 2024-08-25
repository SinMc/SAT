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
    with open("./coordinate.json", "r") as f:
        data = json.load(f)
    for loc in data:
        newpath = str(loc["metadata"]["location"]["latitude"]) + ", " + str(loc["metadata"]["location"]["longitude"])
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        d = loc["severities"]

        for rcp in d:
            # print(rcp)
            r = d[rcp]
            r = {k: v for k, v in r.items() if v !=None}

            fig, axs = plt.subplots(len(r), sharex= True)

            for i, hazard in enumerate(r):
                # print(hazard)
                h = r[hazard]
                # print(h)
                fig.suptitle("Hazards")
                fig.supxlabel("Year", va= "center")
                fig.supylabel("Risk")
                fig.legend(h, loc="outside right")
                axs[i].set_box_aspect(0.17)
                axs[i].set_title(hazard)
                fig.subplots_adjust(hspace=0.5)

                for number in h:
                    # print(number)
                    n = h[number]
                    x = n.keys()
                    y = n.values()
                    axs[i].plot(x,y)

                # print(counter)
            plt.xticks(rotation=30)
            fig.savefig(newpath + f"/graph_{rcp}.png")

    return ["graph.png"]



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

    response_json = []
    for location in locations:
        response = requests.post(url, data= json.dumps(location), headers= headers)
        response_json.append(response.json())
    # print(response_json)
    return response_json


if __name__ == "__main__":
    # called when run from the command line

    if len(sys.argv) < 2:
        print("Please provide a filepath.")
        sys.exit(1)

    filepath = sys.argv[1]
    main(filepath)
