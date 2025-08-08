# Third-party imports
import pytest
from fastapi import status
from tests.fixtures.database import client


@pytest.mark.usefixtures("client", "payload_review")
class TestReviews:

    def test_create_review(self, client, payload_review):
        response = client.post("/reviews/", json=payload_review)
        assert response.status_code == status.HTTP_201_CREATED
