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

