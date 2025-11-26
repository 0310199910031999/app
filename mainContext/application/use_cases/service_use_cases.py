from mainContext.application.ports.ServiceRepo import ServiceRepo
from mainContext.application.dtos.service_dto import ServiceDTO, ServiceCreateDTO, ServiceUpdateDTO
from typing import List, Optional

class CreateService:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo
    
    def execute(self, dto: ServiceCreateDTO) -> int:
        return self.repo.create_service(dto)

class GetServiceById:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo
    
    def execute(self, id: int) -> Optional[ServiceDTO]:
        return self.repo.get_service_by_id(id)

class GetAllServices:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo
    
    def execute(self) -> List[ServiceDTO]:
        return self.repo.get_all_services()

class UpdateService:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo
    
    def execute(self, id: int, dto: ServiceUpdateDTO) -> bool:
        return self.repo.update_service(id, dto)

class DeleteService:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_service(id)
