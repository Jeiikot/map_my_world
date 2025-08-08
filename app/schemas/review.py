# Standard library imports
from datetime import datetime
from typing import Optional

# Third-party imports
from pydantic import BaseModel, ConfigDict


class ReviewCreate(BaseModel):
    location_id: int
    category_id: int
    reviewed_at: Optional[datetime] = None


class Review(BaseModel):
    id: int
    location_id: int
    category_id: int
    reviewed_at: datetime

    model_config = ConfigDict(from_attributes=True)
