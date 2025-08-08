# Third-party imports
import pytest

# Local imports
from app.models.location import LocationModel


@pytest.fixture()
def payload_location(fake):
    return {
        "latitude": fake.pyfloat(min_value=-90, max_value=90),
        "longitude": fake.pyfloat(min_value=-180, max_value=180)
    }


@pytest.fixture()
def payload_locations(fake):
    def factory(count: int):
        return [
            {
                "latitude": fake.pyfloat(min_value=-90, max_value=90),
                "longitude": fake.pyfloat(min_value=-180, max_value=180)
            }
            for _ in range(count)
        ]
    return factory


@pytest.fixture()
def setup_locations(db_session, payload_locations):
    payload_locations = payload_locations(3)

    locations = [LocationModel(**data) for data in payload_locations]
    db_session.add_all(locations)
    db_session.flush()
    location_ids = [location.id for location in locations]

    db_session.commit()
    return location_ids
