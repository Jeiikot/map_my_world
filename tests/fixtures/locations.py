# Third-party imports
import pytest
from sqlalchemy import text


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


@pytest.fixture(scope="function")
def setup_locations(db_session, payload_locations):
    locations = payload_locations(2)
    inserted_ids = []

    for location in locations:
        db_session.execute(
            text("INSERT INTO locations (latitude, longitude) VALUES (:latitude, :longitude)"),
            {"latitude": location.get("latitude"), "longitude": location.get("latitude")}
        )
        row = db_session.execute(text("SELECT last_insert_rowid()")).scalar_one()
        inserted_ids.append(row)

    db_session.commit()
    return inserted_ids
