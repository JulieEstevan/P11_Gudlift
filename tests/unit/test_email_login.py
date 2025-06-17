import pytest
from server import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test the index page."""
    response = client.get('/')
    assert response.status_code == 200


def test_valid_email(client):
    """Test the index page with a valid email."""
    response = client.post('/show_summary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Welcome, Simply Lift' in response.data


def test_no_email(client):
    """Test the index page with no email."""
    response = client.post('/show_summary', data={'email': ''})
    assert response.status_code == 200
    assert b'Please enter your email address' in response.data


def test_invalid_email(client):
    """Test the index page with an invalid email."""
    response = client.post('/show_summary', data={'email': 'invalid-email'})
    assert response.status_code == 200
    assert b'Please enter a valid email address' in response.data


def test_email_not_found(client):
    """Test the index page with an email not found in records."""
    response = client.post('/show_summary', data={'email': 'email@notfound.com'})
    assert response.status_code == 200
    assert b'Email address not found in our records' in response.data
