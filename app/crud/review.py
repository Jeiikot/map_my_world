# Standard library imports
from datetime import datetime, timezone

# Third-party imports
from sqlalchemy.orm import Session

# Local imports
from app.models.review import ReviewModel
from app.schemas.review import ReviewCreate


def create_review(db: Session, review: ReviewCreate):
    review = ReviewModel(
        location_id=review.location_id,
        category_id=review.category_id,
        reviewed_at=review.reviewed_at or datetime.now(timezone.utc)
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
