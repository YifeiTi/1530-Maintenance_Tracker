from datetime import datetime, timezone

from sqlalchemy import text

from app.db import engine


def create_report(description: str, unit_id: int):
    cleaned = description.strip()
    if not cleaned:
        raise ValueError("Description is required")
    if engine is None:
        raise RuntimeError("DATABASE_URL is not set. See backend/.env.example")

    submitted_at = datetime.now(timezone.utc)
    with engine.begin() as conn:
        row = (
            conn.execute(
                text(
                    """
                    INSERT INTO maintenance_requests (unit_id, description, status, submitted_at)
                    VALUES (:unit_id, :description, :status, :submitted_at)
                    RETURNING id, unit_id, description, status, submitted_at
                    """
                ),
                {
                    "unit_id": unit_id,
                    "description": cleaned,
                    "status": "Submitted",
                    "submitted_at": submitted_at,
                },
            )
            .mappings()
            .one()
        )
    return dict(row)
