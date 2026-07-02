from typing import List, Optional
from datetime import date, timedelta
from mainContext.application.dtos.dashboard import (
    DashboardDTO, DateRangeDTO, BestClientsByDateDTO,
    ServicesByDateRangeDTO, BestServicesByDateDTO, MobileClientDashboardDTO,
    SearchByIdDTO,
    SearchByIdResultDTO,
    SearchByIdRequestDTO,
    TechnicianRatingsRequestDTO,
    TechnicianRatingsResultDTO,
)
from mainContext.application.ports.DashboardRepo import DashboardRepo

class DashboardOverview:
    def __init__(self, dashboard_repo: DashboardRepo):
        self.dashboard_repo = dashboard_repo

    def execute(self) -> DashboardDTO:
        return self.dashboard_repo.getDashboard()

class GetBestClientsByDate:
    def __init__(self, dashboard_repo: DashboardRepo):
        self.dashboard_repo = dashboard_repo

    def execute(self, date_range: DateRangeDTO) -> BestClientsByDateDTO:
        return self.dashboard_repo.getBestClientsByDate(date_range)

class GetServicesByDateRange:
    def __init__(self, dashboard_repo: DashboardRepo):
        self.dashboard_repo = dashboard_repo

    def execute(self, date_range: DateRangeDTO) -> ServicesByDateRangeDTO:
        return self.dashboard_repo.getServicesByDateRange(date_range)

class GetBestServicesByDate:
    def __init__(self, dashboard_repo: DashboardRepo):
        self.dashboard_repo = dashboard_repo

    def execute(self, date_range: DateRangeDTO) -> BestServicesByDateDTO:
        return self.dashboard_repo.getBestServicesByDate(date_range)


class GetClientMobileDashboard:
    def __init__(self, dashboard_repo: DashboardRepo):
        self.dashboard_repo = dashboard_repo

    def execute(self, client_id: int) -> MobileClientDashboardDTO:
        return self.dashboard_repo.getClientMobileDashboard(client_id)


class SearchByIdUseCase:
    def __init__(self, dashboard_repo: DashboardRepo):
        self.dashboard_repo = dashboard_repo

    def execute(self, request: SearchByIdRequestDTO) -> SearchByIdResultDTO:
        return self.dashboard_repo.search_by_id(request)


class GetRatingsByTechnician:
    def __init__(self, dashboard_repo: DashboardRepo):
        self.dashboard_repo = dashboard_repo

    def execute(self, request: TechnicianRatingsRequestDTO) -> TechnicianRatingsResultDTO:
        today = date.today()
        start_date = request.start_date
        end_date = request.end_date

        if start_date is None or end_date is None:
            start_of_month = today.replace(day=1)
            end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            if start_date is None:
                start_date = start_of_month
            if end_date is None:
                end_date = end_of_month

        date_range = DateRangeDTO(start_date=start_date, end_date=end_date)
        return self.dashboard_repo.getRatingsByTechnician(date_range)
