from abc import ABC, abstractmethod
from typing import Optional
from mainContext.domain.models.Equipment import Equipment
from mainContext.application.dtos.Equipment.brands_types_dto import BrandsTypesDTO


class EquipmentRepo(ABC):

    @abstractmethod
    def list_by_client_id(self, client_id: str) -> list[Equipment]:
        pass
    @abstractmethod
    def create_equipment(self, equipment: Equipment) -> Optional[Equipment]:
        pass
    @abstractmethod
    def get_equipment_by_id(self, equipment_id: int) -> Optional[Equipment]:
        pass 
    @abstractmethod
    def delete_equipment(self, equipment_id: int) -> bool:
        pass  
    
    @abstractmethod
    def update_equipment(self, equipment_id: int, equipment: Equipment) -> Optional[Equipment]:
        pass

    @abstractmethod
    def get_brands_and_types(self) -> BrandsTypesDTO:
        pass