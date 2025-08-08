# Standard library imports
import datetime

# Third-party imports
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

# Local imports
from app.models.base import Base


class ReviewModel(Base):
    __tablename__ = "location_category_reviewed"

    id: Mapped[int] = mapped_column(primary_key=True)

    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    reviewed_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    location: Mapped["LocationModel"] = relationship("app.models.location.LocationModel")
    category: Mapped["CategoryModel"] = relationship("app.models.category.CategoryModel")
