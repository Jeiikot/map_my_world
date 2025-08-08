# Third-party imports
import pytest
from faker import Faker


@pytest.fixture
def fake():
    return Faker()
