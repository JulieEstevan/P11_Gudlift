from tests.conftest import client


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