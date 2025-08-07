# Standard library imports
from contextlib import asynccontextmanager

# Third-party imports
from fastapi import FastAPI

# Local imports
from app.dependencies import database
from app.routers.locations import router as locations
from app.routers.categories import router as categories
from app.routers.reviews import router as reviews
from app.routers.recommendations import router as recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


def configure_routers(app: FastAPI) -> None:
    app.include_router(locations)
    app.include_router(categories)
    app.include_router(reviews)
    app.include_router(recommendations)



def create_app() -> FastAPI:
    app = FastAPI(
        title="Map My World API",
        description="API to manage locations, categories, and fresh recommendations for Map My World.",
        version="1.0.0",
        lifespan=lifespan
    )

    configure_routers(app)

    return app
