from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:password@localhost:5432/nfactorial", echo=True
)


def get_db():
    with Session(engine) as session:
        yield session
