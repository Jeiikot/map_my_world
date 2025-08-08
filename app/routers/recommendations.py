# Third-party imports
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Local imports
from app import crud
from app.dependencies.session import get_db
from app.schemas.recommendation import Recommendation


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get(
    path="/",
    response_model=list[Recommendation]
)
def get_recommendations(limit:int = 10, db: Session = Depends(get_db)):
    """
    Returns up to 10 location-category combos not reviewed in last 30 days,
    prioritizing combos never reviewed.
    """
    return crud.get_recommendations(db, limit=limit)
