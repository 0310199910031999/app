from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.service_dto import ServiceDTO, ServiceCreateDTO, ServiceUpdateDTO

class ServiceRepo(ABC):
    @abstractmethod
    def create_service(self, dto: ServiceCreateDTO) -> int:
        pass
    
    @abstractmethod
    def get_service_by_id(self, id: int) -> Optional[ServiceDTO]:
        pass
    
    @abstractmethod
    def get_all_services(self) -> List[ServiceDTO]:
        pass
    
    @abstractmethod
    def update_service(self, id: int, dto: ServiceUpdateDTO) -> bool:
        pass
    
    @abstractmethod
    def delete_service(self, id: int) -> bool:
        pass
