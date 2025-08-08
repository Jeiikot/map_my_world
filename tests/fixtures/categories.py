# Third-party imports
import pytest
from sqlalchemy import text

from app.models import CategoryModel


@pytest.fixture()
def payload_category(fake):
    return {"name": fake.word()}


@pytest.fixture()
def payload_categories(fake):
    def factory(count: int):
        return [
            {"name": fake.word()}
            for _ in range(count)
        ]
    return factory


@pytest.fixture()
def setup_categories(db_session, fake, payload_categories):
    payload_categories = payload_categories(3)

    categories = [CategoryModel(**data) for data in payload_categories]
    db_session.add_all(categories)
    db_session.flush()
    category_ids = [category.id for category in categories]

    db_session.commit()
    return category_ids
