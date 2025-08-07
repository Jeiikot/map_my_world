# Third-party imports
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Local imports
from app import crud
from app.dependencies.session import get_db
from app.schemas.location import Location, LocationCreate


router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post(
    path="/",
    response_model=Location,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Location successfully created."
        },
        status.HTTP_409_CONFLICT:{
            "description": "Location with these coordinates already exists.",
            "content": {
                "application/json": {
                    "example": {"detail": "Location with these coordinates already exists."}
                }
            }
        }
    }
)
def add_location(location: LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db, location)

@router.get(
    path="/",
    response_model=list[Location],
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Response."
        }
    }

)
def list_locations(db: Session = Depends(get_db)):
    return crud.get_locations(db)
