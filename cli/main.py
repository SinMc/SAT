"""
[changeme]
"""
import os
import folium.map
import requests
import sys
import json
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import csv
import folium
from PIL import Image
import io
import selenium

filepath = './cli/test/fixtures/test.csv'

def main(input_path):
    locations = retrieve_locations(input_path)
    response = network_request(locations)
    w_temp(response)
    graph(response)
    csvw(response)
    maps(locations)


def w_temp(response_json):
    with open("coordinate.json", "w") as file: 
         file.write(json.dumps(response_json))


def reader():
    with open("./coordinate.json", "r") as f:
        data = json.load(f)
    return data


def maps(locations):
    x, y = zip(*locations)
    map = folium.Map(zoom_control=False)
    map.fit_bounds([[min(x), min(y)], [max(x), max(y)]])

    for location in locations:
        folium.Marker(location=(location), icon=folium.Icon(icon="cloud")).add_to(map)
    map_data = map._to_png()
    img_map = Image.open(io.BytesIO(map_data))
    img_map.save('Map.png')


def csvw(data):
    for loc in data:
        d = loc["severities"]
        name = str(loc["metadata"]["location"]["latitude"]) + ", " + str(loc["metadata"]["location"]["longitude"])

        lst = []
        header = []

        for rcp in d:
            r = d[rcp]
            r = {k: v for k, v in r.items() if v !=None}

            for hazard in r:
                h = r[hazard]

                file_name = name + '/' + rcp + f'/{hazard}_risk.csv'

                with open(file_name, 'w', newline='') as f:
                    writer = csv.writer(f)

                    for likelihood in h:
                        n = h[likelihood]
                        header.clear()
                        header.append("return period")
                        lst.clear()
                        lst.append(likelihood)

                        for key, value in n.items():
                            header.append(key)
                            f.flush()                                
                            lst.append(value)

                        if os.path.getsize(file_name) == 0:
                            writer.writerow(header)
                            
                        writer.writerow(lst)
                



def graph(data):
    for loc in data:
        newpath = str(loc["metadata"]["location"]["latitude"]) + ", " + str(loc["metadata"]["location"]["longitude"])
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        d = loc["severities"]

        for rcp in d:
            r = d[rcp]
            r = {k: v for k, v in r.items() if v !=None}

            f_rcp = newpath + f"/{rcp}"
            if not os.path.exists(f_rcp):
                os.makedirs(f_rcp)

            fig, axs = plt.subplots(len(r), sharex= True)

            for i, hazard in enumerate(r):
                h = r[hazard]
                fig.suptitle("Hazards")
                fig.supxlabel("Year", va= "center")
                fig.supylabel("Risk")
                fig.legend(h, loc="outside right")
                axs[i].set_box_aspect(0.17)
                axs[i].set_title(hazard)
                fig.subplots_adjust(hspace=0.5)

                for likelihood in h:
                    n = h[likelihood]
                    x = n.keys()
                    y = n.values()
                    axs[i].plot(x,y)

            plt.xticks(rotation=30)
            fig.savefig(f_rcp + "/graph.png")



def retrieve_locations(filepath: str):
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    locations = []

    for line in lines[1:]:
        line = line.strip()
        ls = line.split(",") 
        fls = float(ls[0]), float(ls[1])
        locations.append(fls)
    return locations


def network_request(locations):
    f_locations = []
    response_json = []

    url = "https://api.climaterisk.qa/v1/severities"
    api_token = os.environ.get("SEVERITIES_API_TOKEN")
    headers = {"Authorization": "Basic {}".format(api_token)}

    for location in locations:
        f_coord = {"coordinates":{"latitude":location[0],"longitude":location[1]}}
        f_locations.append(f_coord)
    
    for f_location in f_locations:
        response = requests.post(url, data= json.dumps(f_location), headers= headers)
        response_json.append(response.json())
    return response_json


if __name__ == "__main__":
    # called when run from the command line

    if len(sys.argv) < 2:
        print("Please provide a filepath.")
        sys.exit(1)

    filepath = sys.argv[1]
    main(filepath)
