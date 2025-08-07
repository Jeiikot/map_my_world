# Third-party imports
from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    latitude: float
    longitude: float


class Location(BaseModel):
    id: int
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)
