from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.reports.store import create_report, list_active_reports

router = APIRouter()


class ReportIn(BaseModel):
    description: str
    unit_id: UUID


@router.post("/reports")
def submit_report(body: ReportIn):
    try:
        return create_report(body.description, body.unit_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
@router.get("/reports")
def get_active_reports(unit_id: UUID):
    return list_active_reports(unit_id)
