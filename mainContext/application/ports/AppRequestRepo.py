from abc import ABC, abstractmethod
from typing import List, Optional

from mainContext.application.dtos.app_request_dto import (
    AppRequestDTO,
    AppRequestCreateDTO,
    AppRequestUpdateDTO,
    AppRequestCloseDTO,
)


class AppRequestRepo(ABC):
    @abstractmethod
    def create_app_request(self, dto: AppRequestCreateDTO) -> int:
        pass

    @abstractmethod
    def get_app_request_by_id(self, app_request_id: int) -> Optional[AppRequestDTO]:
        pass

    @abstractmethod
    def get_all_app_requests(self) -> List[AppRequestDTO]:
        pass

    @abstractmethod
    def get_app_requests_by_equipment(self, equipment_id: int) -> List[AppRequestDTO]:
        pass

    @abstractmethod
    def update_app_request(self, app_request_id: int, dto: AppRequestUpdateDTO) -> bool:
        pass

    @abstractmethod
    def delete_app_request(self, app_request_id: int) -> bool:
        pass

    @abstractmethod
    def close_app_request(self, app_request_id: int, dto: AppRequestCloseDTO) -> bool:
        pass
