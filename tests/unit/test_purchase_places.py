from tests.conftest import client
from server import clubs, competitions


def test_purchase_more_places_than_club_points_available(client):
    """Test purchasing more places than club points available."""
    response = client.post('/purchase_places', data={
        'competition': 'Summer Showdown',
        'club': 'Simply Lift',
        'places': 10
    })
    assert response.status_code == 400
    assert b'Not enough points available' in response.data


def test_purchase_more_than_12_places(client):
    """Test purchasing more than 12 places."""
    response = client.post('/purchase_places', data={
        'competition': 'Summer Showdown',
        'club': 'Simply Lift',
        'places': 13  # Assuming this exceeds the limit
    })
    assert response.status_code == 400
    assert b'You cannot book more than 12 places' in response.data

def test_purchase_more_places_than_available(client):
    """Test purchasing more places than available in the competition."""
    response = client.post('/purchase_places', data={
        'competition': 'Summer Showdown',
        'club': 'Simply Lift',
        'places': 100  # Assuming this exceeds the available places
    })
    assert response.status_code == 400
    assert b'You cannot book more places than available' in response.data

def test_purchase_places_success(client):
    """Test successful purchase of places."""
    response = client.post('/purchase_places', data={
        'competition': 'Summer Showdown',
        'club': 'Simply Lift',
        'places': 2
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    # Check if the points were decremented correctly
    updated_club = next((c for c in clubs if c['name'] == 'Simply Lift'), None)
    assert updated_club is not None
    assert int(updated_club['points']) == 7  # Assuming initial points were 9 and 2 were decremented

    # Check if the number of places in the competition was decremented correctly
    updated_competition = next((c for c in competitions if c['name'] == 'Summer Showdown'), None)
    assert updated_competition is not None
    assert int(updated_competition['number_of_places']) == 18  # Assuming initial places were 20 and 2 were decremented