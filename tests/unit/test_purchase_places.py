import pytest
from server import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def purchase_valid_places(client):
    """Test the purchase places functionality."""
    response = client.post('/purchase_places', data={
        'competition': 'Summer Showdown',
        'club': 'Simply Lift',
        'places': 2
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    assert b'Summer Showdown Date: 2025-07-10 14:00:00 Number of Places: 18' in response.data  # Assuming this is the number of places available after booking


def test_purchase_more_places_than_club_points_available(client):
    """Test purchasing more places than club points available."""
    response = client.post('/purchase_places', data={
        'competition': 'Summer Showdown',
        'club': 'Simply Lift',
        'places': 20  # Assuming this exceeds club points
    })
    assert response.status_code == 200
    assert b'Not enough points available' in response.data
    assert b'Places available: 20' in response.data  # Assuming this is the number of places available


def test_purchase_more_than_12_places(client):
    """Test purchasing more than 12 places."""
    response = client.post('/purchase_places', data={
        'competition': 'Summer Showdown',
        'club': 'Simply Lift',
        'places': 13  # Assuming this exceeds the limit
    })
    assert response.status_code == 200
    assert b'You cannot book more than 12 places' in response.data
    assert b'Places available: 20' in response.data  # Assuming this is the number of places available