from typing import List
from mainContext.application.dtos.dashboard import DashboardDTO
from mainContext.application.ports.DashboardRepo import DashboardRepo

class DashboardOverview:
    def __init__(self, dashboard_repo: DashboardRepo):
        self.dashboard_repo = dashboard_repo

    def execute(self) -> DashboardDTO:
        return self.dashboard_repo.getDashboard()