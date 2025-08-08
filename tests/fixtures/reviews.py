# Standard library imports
import datetime

# Third-party imports
import pytest


@pytest.fixture()
def payload_review(fake, setup_locations, setup_categories):
    random_dt = fake.date_time_between(start_date="-2y", end_date="now", tzinfo=datetime.timezone.utc)
    reviewed_at = random_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    payload = {
        "location_id": setup_locations[0],
        "category_id": setup_categories[0],
        "reviewed_at": reviewed_at
    }
    return payload

