# Third-party imports
from pydantic import BaseModel, ConfigDict, Field


class LocationCreate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class Location(BaseModel):
    id: int
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)
