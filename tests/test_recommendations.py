# Third-party imports
import pytest
from fastapi import status

@pytest.mark.usefixtures("client", "setup_reviews")
class TestRecommendations:

    def test_recommendations_default(self, client):
        response = client.get("/recommendations/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert isinstance(data, list)
        assert all({"location_id", "category_id", "never_reviewed"} <= set(item) for item in data)

        pairs = [(i["location_id"], i["category_id"]) for i in data]
        assert len(pairs) == len(set(pairs))

        assert any(i["never_reviewed"] is True for i in data)
        assert any(i["never_reviewed"] is False for i in data)

    def test_recommendations_respect_limit(self, client):
        response = client.get("/recommendations/?limit=2")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
