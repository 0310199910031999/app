from fastapi import APIRouter, Depends 
from typing import List
from sqlalchemy.orm import Session
from api.v1.schemas.dashboard import DashboardSchema
from shared.db import get_db

from mainContext.application.use_cases.dashboard_use_cases import DashboardOverview
from mainContext.infrastructure.adapters.DashboardRepo import DashboardRepoImpl


DashboardRouter = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@DashboardRouter.get("/overview", response_model=DashboardSchema)
def dashboard_overview(db: Session = Depends(get_db)):
    repo = DashboardRepoImpl(db)
    use_case = DashboardOverview(repo)
    return use_case.execute()