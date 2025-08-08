# Third-party imports
import pytest
from sqlalchemy import text


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


@pytest.fixture(scope="function")
def setup_categories(db_session, fake, payload_categories):
    categories = payload_categories(2)
    inserted_ids = []

    for category in categories:
        db_session.execute(
            text("INSERT INTO categories (name) VALUES (:name)"),
            {"name": category.get("name")}
        )
        row = db_session.execute(text("SELECT last_insert_rowid()")).scalar_one()
        inserted_ids.append(row)

    db_session.commit()
    return inserted_ids
