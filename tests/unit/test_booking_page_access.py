import pytest
from server import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_booking_page_valid(client):
    """Test the booking page for a specific competition and club."""
    response = client.get('/book/Summer Showdown/Simply Lift')
    assert response.status_code == 200
    assert b'Booking for Summer Showdown' in response.data
    assert b'Simply Lift' in response.data

def test_booking_page_past_competition(client):
    """Test the booking page for a past competition."""
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b'Competition already passed' in response.data