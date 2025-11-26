from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.equipment_brand_dto import EquipmentBrandDTO, EquipmentBrandCreateDTO, EquipmentBrandUpdateDTO

class EquipmentBrandRepo(ABC):
    @abstractmethod
    def create_equipment_brand(self, dto: EquipmentBrandCreateDTO) -> int:
        pass
    
    @abstractmethod
    def get_equipment_brand_by_id(self, id: int) -> Optional[EquipmentBrandDTO]:
        pass
    
    @abstractmethod
    def get_all_equipment_brands(self) -> List[EquipmentBrandDTO]:
        pass
    
    @abstractmethod
    def update_equipment_brand(self, id: int, dto: EquipmentBrandUpdateDTO) -> bool:
        pass
    
    @abstractmethod
    def delete_equipment_brand(self, id: int) -> bool:
        pass
