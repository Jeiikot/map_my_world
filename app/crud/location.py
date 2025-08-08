# Third-party imports
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Local imports
from app.schemas.location import LocationCreate
from app.models.location import LocationModel
from app.utils.exceptions import raise_location_exists


def create_location(db: Session, location: LocationCreate):
    location_exists = db.query(LocationModel).filter(
        LocationModel.longitude == location.longitude,
        LocationModel.latitude == location.latitude
    ).first()

    if location_exists:
        raise_location_exists()

    db_location = LocationModel(**location.model_dump())
    db.add(db_location)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise_location_exists()

    db.refresh(db_location)
    return db_location

def get_locations(db: Session, skip: int = 0, limit: int = 20):
    return db.query(LocationModel).offset(skip).limit(limit).all()
