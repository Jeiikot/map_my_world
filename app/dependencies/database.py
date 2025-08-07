# Third-party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local imports
from app.models.base import BaseModel


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    BaseModel.metadata.create_all(bind=engine)
