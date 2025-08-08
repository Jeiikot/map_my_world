# Standard library imports
import datetime

# Third-party imports
from sqlalchemy.orm import Session
from sqlalchemy import literal, select, func, or_

# Local imports
from app import models
from app.schemas.recommendation import Recommendation


def get_recommendations(db: Session, limit: int = 10) -> list[Recommendation]:
    date_range = datetime.datetime.utcnow() - datetime.timedelta(days=30)

    # Get reviews filtered by location_id, category_id, and date range
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

    base_query = (
        select(
            models.LocationModel.id.label("location_id"),
            models.CategoryModel.id.label("category_id"),
            (last_reviews_subquery.c.last_reviewed_at.is_(None)).label("never_reviewed"),
            last_reviews_subquery.c.last_reviewed_at,
        )
        .select_from(models.LocationModel)
        .join(models.CategoryModel, literal(True))
        .join(
            last_reviews_subquery,
            (models.LocationModel.id == last_reviews_subquery.c.location_id)
            & (models.CategoryModel.id == last_reviews_subquery.c.category_id),
            # Keep all combinations even if no review exists
            isouter=True,
        )
        .where(
            or_(
                last_reviews_subquery.c.last_reviewed_at.is_(None),
                last_reviews_subquery.c.last_reviewed_at < date_range,
            )
        )
        .order_by(
            (last_reviews_subquery.c.last_reviewed_at.is_(None)).desc(),
            last_reviews_subquery.c.last_reviewed_at.asc(),
        )
        .limit(limit)
    )

    results = db.execute(base_query).all()
    return [Recommendation(**recommendation._mapping) for recommendation in results]
