import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Reads DATABASE_URL from backend/.env (never commit that file).
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None


def check_connection():
    """Run SELECT 1 against the Supabase Postgres database."""
    if engine is None:
        raise RuntimeError("DATABASE_URL is not set. See backend/.env.example")
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
