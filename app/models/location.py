# Third-party imports
from sqlalchemy import Float, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

# Local imports
from app.models.base import Base


class LocationModel(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('latitude', 'longitude', name='_location_coordinates_uc'),
        CheckConstraint('latitude BETWEEN -90 AND 90', name='latitude_range'),
        CheckConstraint('longitude BETWEEN -180 AND 180', name='longitude_range'),
    )
