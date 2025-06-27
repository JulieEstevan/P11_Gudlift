from tests.conftest import client


def test_purchase_valid_places(client):
    """Test the purchase places functionality."""
    response = client.post('/purchase_places', data={
        'competition': 'Summer Showdown',
        'club': 'Simply Lift',
        'places': 2
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data


def test_purchase_more_places_than_club_points_available(client):
    """Test purchasing more places than club points available."""
    response = client.post('/purchase_places', data={
        'competition': 'Summer Showdown',
        'club': 'Simply Lift',
        'places': 10  # Assuming this exceeds club points
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
    """Test purchasing more places than available."""
    response = client.post('/purchase_places', data={
        'competition': 'Summer Showdown',
        'club': 'Simply Lift',
        'places': 100  # Assuming this exceeds the available places
    })
    assert response.status_code == 400
    assert b'You cannot book more places than available' in response.data