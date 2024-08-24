import os
import pytest

from cli.main import retrieve_locations, network_request, main, format_output

filepath = './cli/test/fixtures/test.csv'

def test_main():
    assert True
    # files = main(filepath)
    # for file in files:
    #     assert os.path.isfile(file)


def test_read_csv_file():
    known_locations = [
        {'coordinates':{'latitude': -37.7974457951565, 'longitude': 145.07593755525113}},
        {'coordinates':{'latitude': -37.790440, 'longitude': 145.098495}},
        {'coordinates':{'latitude': -33.829724179741305, 'longitude': 151.06481462266254}} 
    ]
    # when
    locations = retrieve_locations(filepath)
    # then
    assert locations == known_locations

def test_format_output():
    graphs = format_output()
    # for graph in graphs:
    #     assert os.path.isfile(graph)


@pytest.mark.slow
def test_test():
    results = network_request()
    assert results[0]['severities']