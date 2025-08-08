# Third-party imports
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Local imports
from app.schemas.category import Category, CategoryCreate
from app.dependencies.session import get_db
from app import crud


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    path="/",
    response_model=Category,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Category successfully created."
        },
        status.HTTP_409_CONFLICT:{
            "description": "Category with this name already exists.",
            "content": {
                "application/json": {
                    "example": {"detail": "Category with this name already exists."}
                }
            }
        }
    }
)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)


@router.get(
    path="/",
    response_model=list[Category],
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Response."
        }
    }
)
def list_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)
