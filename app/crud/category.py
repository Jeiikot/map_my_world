# Third-party imports
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Local imports
from app.models.category import CategoryModel
from app.schemas.category import CategoryCreate
from app.utils.exceptions import raise_category_exists


def create_category(db: Session, category: CategoryCreate):
    category_exists = db.query(CategoryModel).filter(
        CategoryModel.name == category.name,
    ).first()

    if category_exists:
        raise_category_exists()


    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise_category_exists()

    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CategoryModel).offset(skip).limit(limit).all()
