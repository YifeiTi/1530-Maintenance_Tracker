from datetime import datetime, timezone

from sqlalchemy import text

from app.db import engine


def create_report(description: str, unit_id: str):
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

def list_active_reports(unit_id: str):
    if engine is None:
        raise RuntimeError("DATABASE_URL is not set. See backend/.env.example")
    
    with engine.connect() as conn:
        rows = (
            conn.execute(
                text(
                    """
                    SELECT id, unit_id, description, status, created_at AS submitted_at
                    FROM maintenance_requests
                    WHERE unit_id = :unit_id AND status <> 'resolved'
                    ORDER BY created_at DESC
                    """
                ), {"unit_id": unit_id},
            )
            .mappings()
            .all()
        )
    return [dict(r) for r in rows]