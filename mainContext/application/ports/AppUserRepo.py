from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.app_user_dto import (
    AppUserDTO,
    AppUserCreateDTO,
    AppUserUpdateDTO,
    AuthAppUserDTO,
    AppUserAuthResponseDTO,
)

class AppUserRepo(ABC):
    @abstractmethod
    def create_app_user(self, dto: AppUserCreateDTO) -> int:
        pass
    
    @abstractmethod
    def get_app_user_by_id(self, id: int) -> Optional[AppUserDTO]:
        pass
    
    @abstractmethod
    def get_all_app_users(self) -> List[AppUserDTO]:
        pass
    
    @abstractmethod
    def update_app_user(self, id: int, dto: AppUserUpdateDTO) -> bool:
        pass
    
    @abstractmethod
    def delete_app_user(self, id: int) -> bool:
        pass
    
    @abstractmethod
    def get_app_users_by_client(self, client_id: int) -> List[AppUserDTO]:
        pass
    
    @abstractmethod
    def listWithClientName(self) -> List[dict]:
        pass

    @abstractmethod
    def auth_app_user(self, auth_dto: AuthAppUserDTO) -> Optional[AppUserAuthResponseDTO]:
        pass