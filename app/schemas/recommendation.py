# Third-party imports
from pydantic import BaseModel


class Recommendation(BaseModel):
    location_id: int
    category_id: int
    never_reviewed: bool