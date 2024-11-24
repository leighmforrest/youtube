from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from youtube.db.models import Base

current_dir = Path(__file__).resolve().parent

default_database_url = f"sqlite+pysqlite:///{current_dir}/youtube.db"


def init_db(database_url=default_database_url):
    """Initialize"""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    return engine, session
