from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

current_dir = Path(__file__).resolve().parent
default_database_url = f"sqlite+pysqlite:///{current_dir}/youtube.db"


class CustomBase(DeclarativeBase):
    """Base class for all models."""

    pass


def init_db(database_url=default_database_url):
    """Function to manufacture a SQLAlchemy engine and session."""
    engine = create_engine(database_url)
    CustomBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    session = Session()

    return engine, session
