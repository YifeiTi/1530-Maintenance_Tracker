from uuid import UUID

from sqlalchemy import text

from app.db import engine


def create_report(title: str, description: str, unit_id: UUID, tenant_id: UUID):
    title = title.strip()
    description = description.strip()
    if not title:
        raise ValueError("Title is required")
    if not description:
        raise ValueError("Description is required")
    if engine is None:
        raise RuntimeError("DATABASE_URL is not set. See backend/.env.example")

    with engine.begin() as conn:
        row = (
            conn.execute(
                text(
                    """
                    INSERT INTO maintenance_requests (unit_id, tenant_id, title, description, status)
                    VALUES (:unit_id, :tenant_id, :title, :description, 'open')
                    RETURNING id, unit_id, tenant_id, title, description, status,
                              created_at AS submitted_at
                    """
                ),
                {
                    "unit_id": str(unit_id),
                    "tenant_id": str(tenant_id),
                    "title": title,
                    "description": description,
                },
            )
            .mappings()
            .one()
        )
    return dict(row)


def update_report(report_id: UUID, status: str | None, planned_fix_note: str | None):
    if engine is None:
        raise RuntimeError("DATABASE_URL is not set. See backend/.env.example")

    with engine.begin() as conn:
        row = (
            conn.execute(
                text(
                    """
                    UPDATE maintenance_requests
                    SET status = COALESCE(:status, status),
                        planned_fix_note = COALESCE(:planned_fix_note, planned_fix_note),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = :report_id
                    RETURNING *
                    """
                ),
                {
                    "report_id": str(report_id),
                    "status": status,
                    "planned_fix_note": planned_fix_note,
                },
            )
            .mappings()
            .one_or_none()
        )
    if row is None:
        return None
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
