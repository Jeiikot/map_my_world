# Third-party imports
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Local imports
from app import crud
from app.dependencies.session import get_db
from app.schemas.review import Review, ReviewCreate


router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post(
    path="/",
    response_model=Review,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED:{
            "description": "Review successfully created."
        },
    }
)
def add_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, review)
