from mainContext.application.ports.AppUserRepo import AppUserRepo
from mainContext.application.dtos.app_user_dto import (
    AppUserDTO,
    AppUserCreateDTO,
    AppUserUpdateDTO,
    AuthAppUserDTO,
    AppUserAuthResponseDTO,
)
from typing import List, Optional

class CreateAppUser:
    def __init__(self, repo: AppUserRepo):
        self.repo = repo
    
    def execute(self, dto: AppUserCreateDTO) -> int:
        return self.repo.create_app_user(dto)

class GetAppUserById:
    def __init__(self, repo: AppUserRepo):
        self.repo = repo
    
    def execute(self, id: int) -> Optional[AppUserDTO]:
        return self.repo.get_app_user_by_id(id)

class GetAllAppUsers:
    def __init__(self, repo: AppUserRepo):
        self.repo = repo
    
    def execute(self) -> List[AppUserDTO]:
        return self.repo.get_all_app_users()

class GetAppUsersByClient:
    def __init__(self, repo: AppUserRepo):
        self.repo = repo
    
    def execute(self, client_id: int) -> List[AppUserDTO]:
        return self.repo.get_app_users_by_client(client_id)

class UpdateAppUser:
    def __init__(self, repo: AppUserRepo):
        self.repo = repo
    
    def execute(self, id: int, dto: AppUserUpdateDTO) -> bool:
        return self.repo.update_app_user(id, dto)

class DeleteAppUser:
    def __init__(self, repo: AppUserRepo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_app_user(id)


class AuthAppUser:
    def __init__(self, repo: AppUserRepo):
        self.repo = repo

    def execute(self, auth_dto: AuthAppUserDTO) -> Optional[AppUserAuthResponseDTO]:
        return self.repo.auth_app_user(auth_dto)
