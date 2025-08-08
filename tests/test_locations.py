# Third-party imports
from fastapi import status
import pytest

# Local imports
from tests.fixtures.database import client


@pytest.fixture()
def payload_location(fake):
    payload = {
        "latitude": fake.pyfloat(min_value=-90, max_value=90),
        "longitude": fake.pyfloat(min_value=-180, max_value=180)
    }
    return payload


@pytest.mark.usefixtures("client", "payload_location")
class TestLocations:

    def test_create_location(self, client, payload_location):
        response = client.post("/locations/", json=payload_location)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["latitude"] == payload_location.get("latitude")
        assert data["longitude"] == payload_location.get("longitude")

    def test_list_locations(self, client, payload_location):
        client.post("/locations/", json=payload_location)
        response = client.get("/locations/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert any(
            location["latitude"] == pytest.approx(payload_location.get("latitude")) and
            location["longitude"] == pytest.approx(payload_location.get("longitude"))
            for location in data
        )
    def test_create_location_conflict(self, client, payload_location):
        response = client.post("/locations/", json=payload_location)
        assert response.status_code == status.HTTP_201_CREATED

        response = client.post("/locations/", json=payload_location)
        assert response.status_code ==  status.HTTP_409_CONFLICT
