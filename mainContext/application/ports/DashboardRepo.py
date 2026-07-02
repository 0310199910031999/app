from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.dashboard import (
    DashboardDTO,
    DateRangeDTO,
    BestClientsByDateDTO,
    ServicesByDateRangeDTO,
    BestServicesByDateDTO,
    MobileClientDashboardDTO,
    SearchByIdDTO,
    SearchByIdResultDTO,
    SearchByIdRequestDTO,
    TechnicianRatingsResultDTO,
)

class DashboardRepo(ABC):
    @abstractmethod
    def getDashboard(self) -> DashboardDTO:
        pass
    
    @abstractmethod
    def getBestClientsByDate(self, date_range: DateRangeDTO) -> BestClientsByDateDTO:
        pass
    
    @abstractmethod
    def getServicesByDateRange(self, date_range: DateRangeDTO) -> ServicesByDateRangeDTO:
        pass
    
    @abstractmethod
    def getBestServicesByDate(self, date_range: DateRangeDTO) -> BestServicesByDateDTO:
        pass

    @abstractmethod
    def getClientMobileDashboard(self, client_id: int) -> MobileClientDashboardDTO:
        pass

    @abstractmethod
    def search_by_id(self, request: SearchByIdRequestDTO) -> SearchByIdResultDTO:
        pass

    @abstractmethod
    def getRatingsByTechnician(self, date_range: DateRangeDTO) -> TechnicianRatingsResultDTO:
        pass
