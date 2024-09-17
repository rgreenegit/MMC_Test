import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    # Check if the response returns valid data, assuming it's a list of bands
    assert isinstance(response.json(), list)


@pytest.mark.parametrize("prefix, expected_band", [
    ("rad", "Radiohead"),
    ("T", "Taylor Swift"),
])
def test_autocomplete_suggest_band(prefix, expected_band):
    response = client.get(f"/autocomplete/?prefix={prefix}")
    assert response.status_code == 200
    suggestions = response.json()
    assert expected_band in suggestions


@pytest.mark.parametrize("prefix, band, expected_album", [
    ("The", "Radiohead", "The King of Limbs"),
    ("Fe", "Taylor Swift", "Fearless"),
])
def test_autocomplete_suggest_album(prefix, band, expected_album):
    response = client.get(f"/autocomplete/?prefix={prefix}&bandName={band}")
    assert response.status_code == 200
    suggestions = response.json()
    assert expected_album in suggestions


@pytest.mark.parametrize("prefix, band, album, expected_song", [
    ("My", "Portishead", "Dummy", "Mysterons"),
    ("S", "Rammstein", "Mutter", "Sonne"),
    ("s", "rammstein", "mutter", "Spieluhr"),
])
def test_autocomplete_suggest_song(prefix, band, album, expected_song):
    response = client.get(
        f"/autocomplete/?prefix={prefix}&bandName={band}&albumTitle={album}")
    assert response.status_code == 200
    suggestions = response.json()
    assert expected_song in suggestions
