from uuid import UUID

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from app.reports import store

router = APIRouter()


class ReportIn(BaseModel):
    title: str
    description: str
    unit_id: UUID
    tenant_id: UUID


class ReportUpdate(BaseModel):
    status: str | None = None
    planned_fix_note: str | None = None


@router.post("/reports")
def submit_report(body: ReportIn):
    try:
        return store.create_report(body.title, body.description, body.unit_id, body.tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/reports")
def get_active_reports(unit_id: UUID):
    return store.list_active_reports(unit_id)


@router.patch("/reports/{report_id}")
def patch_report(report_id: UUID, body: ReportUpdate, x_user_role: str | None = Header(default=None)):
    if x_user_role != "landlord":
        raise HTTPException(status_code=403, detail="Only landlords can update reports")
    if "status" in body.model_fields_set and body.status not in ("in_progress", "resolved"):
        raise HTTPException(status_code=422, detail="Status must be in_progress or resolved")
    if body.status is None and body.planned_fix_note is None:
        raise HTTPException(status_code=422, detail="Provide a status or planned fix note")

    report = store.update_report(report_id, body.status, body.planned_fix_note)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.get("/reports/{report_id}")
def read_report(report_id: UUID):
    report = store.get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report