from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.reports.store import create_report

router = APIRouter()


class ReportIn(BaseModel):
    description: str
    unit_id: int


@router.post("/reports")
def submit_report(body: ReportIn):
    try:
        return create_report(body.description, body.unit_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
