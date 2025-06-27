import pytest
from server import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class MockData:
    """Fixture to provide a mock database."""

    # Mocked data to replace the content of "clubs"
    mock_clubs = [
        {"name": "Club 1", "email": "club1@example.com", "points": "9"},
        {"name": "Club 2", "email": "club2@example.com", "points": "20"},
        {"name": "Club 3", "email": "club3@example.com", "points": "0"}
    ]

    # Mocked data to replace the content of "competitions"
    mock_competitions = [
        {
            "name": "Competition 1",
            "date": "2030-01-01 13:00:00",
            "number_of_places": "25"
        },
        {
            "name": "Competition 2",
            "date": "2030-01-01 13:00:00",
            "number_of_places": "10"
        },
        {
            "name": "Competition 3",
            "date": "2000-01-01 13:00:00",
            "number_of_places": "10"
        },
        {
            "name": "Competition 4",
            "date": "2030-01-01 13:00:00",
            "number_of_places": "0"
        }
    ]

    # Mocked data to have invalid data
    invalid_email = "invalid@example.com"
    invalid_club_name = "invalid_club_name"
    invalid_competition_name = "invalid_competition_name"
    invalid_place_required = "invalid_place_required"