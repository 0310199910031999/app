from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.app_version_dto import AppVersionDTO, AppVersionCreateDTO, AppVersionUpdateDTO

class AppVersionRepo(ABC):
    @abstractmethod
    def create_app_version(self, dto: AppVersionCreateDTO) -> int:
        pass

    @abstractmethod
    def get_app_version_by_id(self, id: int) -> Optional[AppVersionDTO]:
        pass

    @abstractmethod
    def get_all_app_versions(self) -> List[AppVersionDTO]:
        pass

    @abstractmethod
    def update_app_version(self, id: int, dto: AppVersionUpdateDTO) -> bool:
        pass

    @abstractmethod
    def delete_app_version(self, id: int) -> bool:
        pass

    @abstractmethod
    def get_latest_version_number(self) -> Optional[float]:
        pass
