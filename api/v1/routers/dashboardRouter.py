from fastapi import APIRouter, Depends 
from typing import List
from sqlalchemy.orm import Session
from api.v1.schemas.dashboard import (
    DashboardSchema,
    DateRangeSchema,
    BestClientsByDateSchema,
    ServicesByDateRangeSchema,
    BestServicesByDateSchema,
    MobileClientDashboardSchema,
)
from shared.db import get_db

from mainContext.application.use_cases.dashboard_use_cases import (
    DashboardOverview,
    GetBestClientsByDate,
    GetServicesByDateRange,
    GetBestServicesByDate,
    GetClientMobileDashboard,
)
from mainContext.application.dtos.dashboard import DateRangeDTO
from mainContext.infrastructure.adapters.DashboardRepo import DashboardRepoImpl


DashboardRouter = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@DashboardRouter.get("/overview", response_model=DashboardSchema)
def dashboard_overview(db: Session = Depends(get_db)):
    repo = DashboardRepoImpl(db)
    use_case = DashboardOverview(repo)
    return use_case.execute()

@DashboardRouter.post("/best-clients", response_model=BestClientsByDateSchema)
def get_best_clients_by_date(date_range: DateRangeSchema, db: Session = Depends(get_db)):
    repo = DashboardRepoImpl(db)
    use_case = GetBestClientsByDate(repo)
    date_range_dto = DateRangeDTO(start_date=date_range.start_date, end_date=date_range.end_date)
    return use_case.execute(date_range_dto)

@DashboardRouter.post("/services-by-date", response_model=ServicesByDateRangeSchema)
def get_services_by_date_range(date_range: DateRangeSchema, db: Session = Depends(get_db)):
    repo = DashboardRepoImpl(db)
    use_case = GetServicesByDateRange(repo)
    date_range_dto = DateRangeDTO(start_date=date_range.start_date, end_date=date_range.end_date)
    return use_case.execute(date_range_dto)

@DashboardRouter.post("/best-services", response_model=BestServicesByDateSchema)
def get_best_services_by_date(date_range: DateRangeSchema, db: Session = Depends(get_db)):
    repo = DashboardRepoImpl(db)
    use_case = GetBestServicesByDate(repo)
    date_range_dto = DateRangeDTO(start_date=date_range.start_date, end_date=date_range.end_date)
    return use_case.execute(date_range_dto)


@DashboardRouter.get("/mobile/{client_id}", response_model=MobileClientDashboardSchema)
def get_mobile_dashboard(client_id: int, db: Session = Depends(get_db)):
    repo = DashboardRepoImpl(db)
    use_case = GetClientMobileDashboard(repo)
    return use_case.execute(client_id)
