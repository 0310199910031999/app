from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.role_dto import RoleDTO, RoleCreateDTO, RoleUpdateDTO

class RoleRepo(ABC):
    @abstractmethod
    def create_role(self, dto: RoleCreateDTO) -> int:
        pass
    
    @abstractmethod
    def get_role_by_id(self, id: int) -> Optional[RoleDTO]:
        pass
    
    @abstractmethod
    def get_all_roles(self) -> List[RoleDTO]:
        pass
    
    @abstractmethod
    def update_role(self, id: int, dto: RoleUpdateDTO) -> bool:
        pass
    
    @abstractmethod
    def delete_role(self, id: int) -> bool:
        pass
