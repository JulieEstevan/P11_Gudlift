from tests.conftest import client


def test_points_board_page(client):
    """Test the clubs points board page."""
    response = client.get('/clubs_points')
    assert response.status_code == 200