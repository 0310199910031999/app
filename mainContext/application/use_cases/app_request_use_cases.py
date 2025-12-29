from typing import List, Optional

from mainContext.application.ports.AppRequestRepo import AppRequestRepo
from mainContext.application.dtos.app_request_dto import (
    AppRequestDTO,
    AppRequestCreateDTO,
    AppRequestUpdateDTO,
    AppRequestCloseDTO,
)


class CreateAppRequest:
    def __init__(self, repo: AppRequestRepo):
        self.repo = repo

    def execute(self, dto: AppRequestCreateDTO) -> int:
        return self.repo.create_app_request(dto)


class GetAppRequestById:
    def __init__(self, repo: AppRequestRepo):
        self.repo = repo

    def execute(self, app_request_id: int) -> Optional[AppRequestDTO]:
        return self.repo.get_app_request_by_id(app_request_id)


class GetAllAppRequests:
    def __init__(self, repo: AppRequestRepo):
        self.repo = repo

    def execute(self) -> List[AppRequestDTO]:
        return self.repo.get_all_app_requests()


class UpdateAppRequest:
    def __init__(self, repo: AppRequestRepo):
        self.repo = repo

    def execute(self, app_request_id: int, dto: AppRequestUpdateDTO) -> bool:
        return self.repo.update_app_request(app_request_id, dto)


class DeleteAppRequest:
    def __init__(self, repo: AppRequestRepo):
        self.repo = repo

    def execute(self, app_request_id: int) -> bool:
        return self.repo.delete_app_request(app_request_id)


class CloseAppRequest:
    def __init__(self, repo: AppRequestRepo):
        self.repo = repo

    def execute(self, app_request_id: int, dto: AppRequestCloseDTO) -> bool:
        return self.repo.close_app_request(app_request_id, dto)
