# Third-party imports
from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str


class Category(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
