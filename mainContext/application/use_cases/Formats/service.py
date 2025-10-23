from mainContext.application.ports.Formats.service_repo import ServiceRepo
from mainContext.application.dtos.Formats.service_dto import ServiceCreateDTO, ServiceUpdateDTO, ServiceTableRowDTO, ServicesFormatList
from mainContext.domain.models.Formats.Service import Service

from typing import List

class CreateService:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo

    def execute(self, dto: ServiceCreateDTO) -> int:
        return self.repo.create_service(dto)

class GetServiceById:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo

    def execute(self, id: int) -> Service:
        return self.repo.get_service_by_id(id)

class DeleteService:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo

    def execute(self, id: int) -> bool:
        return self.repo.delete_service(id)

class UpdateService:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo

    def execute(self, id: int, dto: ServiceUpdateDTO) -> bool:
        return self.repo.update_service(id, dto)

class GetListServices:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo

    def execute(self) -> List[ServiceTableRowDTO]:
        return self.repo.get_list_services()

class GetSPServices:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo

    def execute(self) -> List[ServicesFormatList]:
        return self.repo.get_sp_services()

class GetSCServices:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo

    def execute(self) -> List[ServicesFormatList]:
        return self.repo.get_sc_services()

class GetOSServices:
    def __init__(self, repo: ServiceRepo):
        self.repo = repo

    def execute(self) -> List[ServicesFormatList]:
        return self.repo.get_os_services()