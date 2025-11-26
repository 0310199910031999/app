from mainContext.application.ports.RoleRepo import RoleRepo
from mainContext.application.dtos.role_dto import RoleDTO, RoleCreateDTO, RoleUpdateDTO
from typing import List, Optional

class CreateRole:
    def __init__(self, repo: RoleRepo):
        self.repo = repo
    
    def execute(self, dto: RoleCreateDTO) -> int:
        return self.repo.create_role(dto)

class GetRoleById:
    def __init__(self, repo: RoleRepo):
        self.repo = repo
    
    def execute(self, id: int) -> Optional[RoleDTO]:
        return self.repo.get_role_by_id(id)

class GetAllRoles:
    def __init__(self, repo: RoleRepo):
        self.repo = repo
    
    def execute(self) -> List[RoleDTO]:
        return self.repo.get_all_roles()

class UpdateRole:
    def __init__(self, repo: RoleRepo):
        self.repo = repo
    
    def execute(self, id: int, dto: RoleUpdateDTO) -> bool:
        return self.repo.update_role(id, dto)

class DeleteRole:
    def __init__(self, repo: RoleRepo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_role(id)
