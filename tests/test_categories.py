# Third-party imports
import pytest
from fastapi import status

# Local imports
from tests.fixtures.database import client


@pytest.fixture()
def payload_category(fake):
    return {"name": fake.word()}


@pytest.mark.usefixtures("client", "payload_category")
class TestCategories:

    def test_create_category(self, client, payload_category):
        response = client.post("/categories/", json=payload_category)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == payload_category.get("name")

    def test_list_categories(self, client, payload_category):
        client.post("/categories/", json=payload_category)
        response = client.get("/categories/")

        assert response.status_code == status.HTTP_200_OK
        categories = response.json()
        assert any(category["name"] == payload_category.get("name") for category in categories)

    def test_create_category_conflict(self, client, payload_category):
        response = client.post("/categories/", json=payload_category)
        assert response.status_code == status.HTTP_201_CREATED

        response = client.post("/categories/", json=payload_category)
        assert response.status_code == status.HTTP_409_CONFLICT
