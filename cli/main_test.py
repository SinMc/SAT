from cli.main import retrieve_locations

def test_read_csv_file():
    # given
    filepath = './cli/test/fixtures/test.csv'
    known_locations = [{'lat': -37.7974457951565, 'lon': 145.07593755525113}, {'lat': -37.790440, 'lon': 145.098495}]
    # when
    locations = retrieve_locations(filepath)
    # then
    assert locations == known_locations
