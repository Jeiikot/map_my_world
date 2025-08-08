# Third-party imports
from sqlalchemy import Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

# Local imports
from app.models.base import Base


class LocationModel(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    __table_args__ = (UniqueConstraint('latitude', 'longitude', name='_location_coordinates_uc'),)
