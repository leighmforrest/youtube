from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from youtube.db.models import CustomBase

current_dir = Path(__file__).resolve().parent
default_database_url = f"sqlite+pysqlite:///{current_dir}/youtube.db"


def one_day_ago():
    return datetime.now(timezone.utc) - timedelta(days=1)


def init_db(database_url=default_database_url):
    """Initialize engine and session."""
    engine = create_engine(database_url)
    CustomBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    session = Session()

    return engine, session
