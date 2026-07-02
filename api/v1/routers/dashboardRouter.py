from fastapi import APIRouter, Depends 
from typing import List, Optional
from api.v1.schemas.dashboard import (
    DashboardSchema,
    DateRangeSchema,
    BestClientsByDateSchema,
    ServicesByDateRangeSchema,
    BestServicesByDateSchema,
    MobileClientDashboardSchema,
    SearchByIdSchema,
    SearchByIdResultSchema,
    SearchByIdRequestSchema,
    TechnicianRatingsRequestSchema,
    TechnicianRatingsResultSchema,
)

from mainContext.application.use_cases.dashboard_use_cases import (
    DashboardOverview,
    GetBestClientsByDate,
    GetServicesByDateRange,
    GetBestServicesByDate,
    GetClientMobileDashboard,
    SearchByIdUseCase,
    GetRatingsByTechnician,
)
from mainContext.application.dtos.dashboard import DateRangeDTO, TechnicianRatingsRequestDTO
from mainContext.infrastructure.dependencies import get_dashboard_repo
from mainContext.infrastructure.adapters.DashboardRepo import DashboardRepoImpl


DashboardRouter = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@DashboardRouter.get("/overview", response_model=DashboardSchema)
def dashboard_overview(repo: DashboardRepoImpl = Depends(get_dashboard_repo)):
    use_case = DashboardOverview(repo)
    return use_case.execute()

@DashboardRouter.post("/best-clients", response_model=BestClientsByDateSchema)
def get_best_clients_by_date(date_range: DateRangeSchema, repo: DashboardRepoImpl = Depends(get_dashboard_repo)):
    use_case = GetBestClientsByDate(repo)
    date_range_dto = DateRangeDTO(start_date=date_range.start_date, end_date=date_range.end_date)
    return use_case.execute(date_range_dto)

@DashboardRouter.post("/services-by-date", response_model=ServicesByDateRangeSchema)
def get_services_by_date_range(date_range: DateRangeSchema, repo: DashboardRepoImpl = Depends(get_dashboard_repo)):
    use_case = GetServicesByDateRange(repo)
    date_range_dto = DateRangeDTO(start_date=date_range.start_date, end_date=date_range.end_date)
    return use_case.execute(date_range_dto)

@DashboardRouter.post("/best-services", response_model=BestServicesByDateSchema)
def get_best_services_by_date(date_range: DateRangeSchema, repo: DashboardRepoImpl = Depends(get_dashboard_repo)):
    use_case = GetBestServicesByDate(repo)
    date_range_dto = DateRangeDTO(start_date=date_range.start_date, end_date=date_range.end_date)
    return use_case.execute(date_range_dto)


@DashboardRouter.get("/mobile/{client_id}", response_model=MobileClientDashboardSchema)
def get_mobile_dashboard(client_id: int, repo: DashboardRepoImpl = Depends(get_dashboard_repo)):
    use_case = GetClientMobileDashboard(repo)
    return use_case.execute(client_id)


@DashboardRouter.get("/search", response_model=SearchByIdResultSchema)
def search_by_id(record_id: Optional[int] = None, file_id: Optional[str] = None, format: Optional[str] = None, repo: DashboardRepoImpl = Depends(get_dashboard_repo)):
    from mainContext.application.dtos.dashboard import SearchByIdRequestDTO
    use_case = SearchByIdUseCase(repo)
    request = SearchByIdRequestDTO(record_id=record_id, file_id=file_id, format_filter=format)
    result = use_case.execute(request)
    return result


@DashboardRouter.post("/ratings-by-technician", response_model=TechnicianRatingsResultSchema)
def get_ratings_by_technician(request: TechnicianRatingsRequestSchema, repo: DashboardRepoImpl = Depends(get_dashboard_repo)):
    use_case = GetRatingsByTechnician(repo)
    request_dto = TechnicianRatingsRequestDTO(start_date=request.start_date, end_date=request.end_date)
    return use_case.execute(request_dto)
