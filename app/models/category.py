# Third-party imports
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

# Local imports
from app.models.base import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=True)
