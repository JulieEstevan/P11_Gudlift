import pytest
from server import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_booking_page(client):
    """Test the booking page for a specific competition and club."""
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b'Booking for Spring Festival' in response.data
    assert b'Simply Lift' in response.data


def purchase_valid_places(client):
    """Test the purchase places functionality."""
    response = client.post('/purchase_places', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 2
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data


def test_purchase_more_places_than_club_points_available(client):
    """Test purchasing more places than club points available."""
    response = client.post('/purchase_places', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 20  # Assuming this exceeds club points
    })
    assert response.status_code == 200
    assert b'Not enough points available' in response.data
