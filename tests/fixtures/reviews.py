# Standard library imports
import datetime

# Third-party imports
import pytest

# Local imports
from app.models.review import ReviewModel


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
def recent_review_dt(fake):
    return fake.date_time_between(start_date="-29d", end_date="now", tzinfo=datetime.timezone.utc)


@pytest.fixture()
def old_review_dt(fake):
    return fake.date_time_between(start_date="-2y", end_date="-30d", tzinfo=datetime.timezone.utc)


@pytest.fixture()
def payload_recent_reviews(setup_locations, setup_categories, recent_review_dt):
    def factory(count: int):
        pairs_count = min(count, len(setup_locations), len(setup_categories))
        return [
            {
                "location_id": location_id,
                "category_id": category_id,
                "reviewed_at": recent_review_dt,
            }
            for location_id, category_id in zip(setup_locations[:pairs_count], setup_categories[:pairs_count])
        ]
    return factory


@pytest.fixture()
def payload_old_reviews(setup_locations, setup_categories, old_review_dt):
    def factory(count: int):
        shifted_categories = setup_categories[1:] + setup_categories[:1]
        pairs_count = min(count, len(setup_locations), len(shifted_categories))
        return [
            {
                "location_id": location_id,
                "category_id": category_id,
                "reviewed_at": old_review_dt,
            }
            for location_id, category_id in zip(setup_locations[:pairs_count], shifted_categories[:pairs_count])
        ]
    return factory


@pytest.fixture()
def setup_reviews(db_session, payload_old_reviews, payload_recent_reviews):
    payload_reviews = payload_old_reviews(1) + payload_recent_reviews(1)

    reviews = [ReviewModel(**row) for row in payload_reviews]
    db_session.add_all(reviews)
    db_session.flush()
    review_ids = [review.id for review in reviews]
    db_session.commit()

    return review_ids
