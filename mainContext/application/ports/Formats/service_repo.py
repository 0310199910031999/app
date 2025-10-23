from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.Service import Service
from mainContext.application.dtos.Formats.service_dto import ServiceCreateDTO, ServiceUpdateDTO, ServiceTableRowDTO, ServicesFormatList
from typing import List

class ServiceRepo(ABC):
    @abstractmethod
    def create_service(self, service: ServiceCreateDTO) -> int:
        pass
    @abstractmethod
    def get_service_by_id(self, id: int) -> Service:
        pass
    @abstractmethod
    def delete_service(self, id: int) -> bool:
        pass
    @abstractmethod
    def update_service(self, id: int, service: ServiceUpdateDTO) -> bool:
        pass
    @abstractmethod
    def get_list_services(self) -> List[ServiceTableRowDTO]:
        pass
    @abstractmethod
    def get_sp_services(self) -> List[ServicesFormatList]:
        pass
    @abstractmethod
    def get_sc_services(self) -> List[ServicesFormatList]:
        pass
    @abstractmethod
    def get_os_services(self) -> List[ServicesFormatList]:
        pass
    