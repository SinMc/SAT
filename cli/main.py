"""
[changeme]
"""
import os
import requests
import sys


def main(input_path):
    # called directly by the flask app
    """
    [Read the input file and return a list of output files]
    """

    
    return ["Octocat.png", "Octocat.png"]  # test output

def retrieve_locations(filepath: str):
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()  # read the file

    locations = []

    for line in lines[1:]:
        separatedcoords = line.split(",") # separates the coordinate values
        lat = float(separatedcoords[0].strip())
        lon = float(separatedcoords[1].strip())
        n_coordinate = {'lat': lat, 'lon': lon}
        locations.append(n_coordinate)
    return locations


def network_request():
    print("\n\n $$$$$ \n\n")
    url = "https://api.climaterisk.qa/v1/severities"
    api_token = os.environ.get("SEVERITIES_API_TOKEN")
    headers = {"Authorization": "Basic {}".format(api_token)}
    data = "{\"coordinates\":{\"latitude\":-32.92874606286358,\"longitude\":151.7829704479731}}"
    response = requests.post(url, data= data, headers= headers)
    response_json = response.json()
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
