"""
[changeme]
"""

import sys


def main(input_path):
    # called directly by the flask app
    """
    [Read the input file and return a list of output files]
    """

    
    return ["Octocat.png", "Octocat.png"]  # test output

def retrieve_locations(filepath: str):
    print("\n\n $$$$$ \n\n")
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


if __name__ == "__main__":
    # called when run from the command line

    if len(sys.argv) < 2:
        print("Please provide a filepath.")
        sys.exit(1)

    filepath = sys.argv[1]
    main(filepath)
