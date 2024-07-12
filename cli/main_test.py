from cli.main import retrieve_locations

def test_read_csv_file():
    # given
    filepath = './cli/test/fixtures/test.csv'
    known_location = {'lat': -37.7974457951565, 'lon': 145.07593755525113}
    # when
    locations = retrieve_locations(filepath)
    # then
    assert locations == [known_location]
