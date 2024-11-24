from pathlib import Path

from sqlalchemy import create_engine

current_dir = Path(__file__).resolve().parent

default_database_url = f"sqlite+pysqlite:///{current_dir}/youtube.db"

engine = create_engine(default_database_url, echo=True)
