from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.dashboard import DashboardDTO

class DashboardRepo(ABC):
    @abstractmethod
    def getDashboard(self) -> DashboardDTO:
        pass