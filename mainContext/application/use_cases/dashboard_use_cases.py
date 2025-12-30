from typing import List
from mainContext.application.dtos.dashboard import (
    DashboardDTO, DateRangeDTO, BestClientsByDateDTO, 
    ServicesByDateRangeDTO, BestServicesByDateDTO, MobileClientDashboardDTO
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
