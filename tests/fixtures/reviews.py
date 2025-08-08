# Standard library imports
import datetime

# Third-party imports
import pytest
from sqlalchemy import text


@pytest.fixture()
def payload_review(fake, setup_locations, setup_categories):
    random_dt = fake.date_time_between(start_date="-29d", end_date="now", tzinfo=datetime.timezone.utc)
    reviewed_at = random_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    payload = {
        "location_id": setup_locations[0],
        "category_id": setup_categories[0],
        "reviewed_at": reviewed_at
    }
    return payload

@pytest.fixture()
def get_recent_review_at(fake):
    random_dt = fake.date_time_between(start_date="-29d", end_date="now", tzinfo=datetime.timezone.utc)
    return random_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

@pytest.fixture()
def get_old_review_at(fake):
    random_dt = fake.date_time_between(start_date="-2y", end_date="-30d", tzinfo=datetime.timezone.utc)
    return random_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

@pytest.fixture()
def payload_recent_reviews(setup_locations, setup_categories, get_recent_review_at):
    def factory(count: int):
        return [
            {
                "location_id": setup_locations[index],
                "category_id": setup_categories[index],
                "reviewed_at": get_recent_review_at,
            }
            for index in range(count)
        ]
    return factory

@pytest.fixture()
def payload_old_reviews(setup_locations, setup_categories, get_old_review_at):
    def factory(count: int):
        return [
            {
                "location_id": setup_locations[index + 1],
                "category_id": setup_categories[index + 1],
                "reviewed_at": get_old_review_at,
            }
            for index in range(count)
        ]
    return factory


@pytest.fixture()
def setup_reviews(db_session, fake, payload_old_reviews, payload_recent_reviews):
    old_reviews = payload_old_reviews(1)
    recent_reviews = payload_recent_reviews(1)
    all_reviews = old_reviews + recent_reviews

    inserted_ids = []

    for review in all_reviews:
        db_session.execute(
            text(
                "INSERT INTO location_category_reviewed (location_id, category_id, reviewed_at) "
                "VALUES (:location_id, :category_id, :reviewed_at)"
            ),
            review
        )
        row = db_session.execute(text("SELECT last_insert_rowid()")).scalar_one()
        inserted_ids.append(row)

    db_session.commit()
