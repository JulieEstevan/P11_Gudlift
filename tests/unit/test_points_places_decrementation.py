from tests.conftest import client
from tests.conftest import MockData


def test_points_decrementation(client, mocker):
    """Test the points decrementation for a specific club."""
    mocker.patch('server.clubs', MockData.mock_clubs)
    mocker.patch('server.competitions', MockData.mock_competitions)

    response = client.post('/purchase_places', data={
        'competition': 'Competition 1',
        'club': 'Club 1',
        'places': 2
    })

    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    # Check if the points were decremented correctly
    updated_club = next((c for c in MockData.mock_clubs if c['name'] == 'Club 1'), None)
    assert updated_club is not None
    assert int(updated_club['points']) == 7  # Assuming initial points were 9 and 2 were decremented


def test_places_decrementation(client, mocker):
    """Test the places decrementation for a specific competition."""
    mocker.patch('server.clubs', MockData.mock_clubs)
    mocker.patch('server.competitions', MockData.mock_competitions)

    response = client.post('/purchase_places', data={
        'competition': 'Competition 2',
        'club': 'Club 1',
        'places': 2
    })

    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    # Check if the number of places was decremented correctly
    updated_competition = next((c for c in MockData.mock_competitions if c['name'] == 'Competition 2'), None)
    assert updated_competition is not None
    assert int(updated_competition['number_of_places']) == 8  # Assuming initial places were 25 and 2 were decremented