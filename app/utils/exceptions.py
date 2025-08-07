# Third-party imports
from fastapi import HTTPException, status


def raise_location_exists():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Location with these coordinates already exists.",
    )

def raise_category_exists():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Category with this name already exists."
    )
