# Standard library imports
import datetime

# Third-party imports
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import literal

# Local imports
from app import models
from app.schemas.recommendation import Recommendation


def get_recommendations(db: Session, limit: int = 10) -> list[Recommendation]:
    date_range = datetime.datetime.utcnow() - datetime.timedelta(days=30)

    last_reviews_subquery = (
        db.query(
            models.ReviewModel.location_id,
            models.ReviewModel.category_id,
            func.max(models.ReviewModel.reviewed_at).label('last_reviewed_at')
        )
        .group_by(
            models.ReviewModel.location_id,
            models.ReviewModel.category_id
        )
        .subquery()
    )

    recommendations_query = (db.query(
        models.LocationModel.id.label('location_id'),
        models.CategoryModel.id.label('category_id'),
        (last_reviews_subquery.c.last_reviewed_at.is_(None)).label('never_reviewed')
    ).select_from(models.LocationModel).join(models.CategoryModel, literal(True)).outerjoin(
        last_reviews_subquery,
        (models.LocationModel.id == last_reviews_subquery.c.location_id) &
        (models.CategoryModel.id == last_reviews_subquery.c.category_id)
    ).filter(
        (last_reviews_subquery.c.last_reviewed_at.is_(None)) |
        (last_reviews_subquery.c.last_reviewed_at < date_range)
    ).order_by(
        (last_reviews_subquery.c.last_reviewed_at.is_(None)).desc(),
        last_reviews_subquery.c.last_reviewed_at.asc()
    ).limit(limit))

    results = recommendations_query.all()
    return [Recommendation(**recommendation._mapping) for recommendation in results]
