from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.equipment_type_dto import EquipmentTypeDTO, EquipmentTypeCreateDTO, EquipmentTypeUpdateDTO

class EquipmentTypeRepo(ABC):
    @abstractmethod
    def create_equipment_type(self, dto: EquipmentTypeCreateDTO) -> int:
        pass
    
    @abstractmethod
    def get_equipment_type_by_id(self, id: int) -> Optional[EquipmentTypeDTO]:
        pass
    
    @abstractmethod
    def get_all_equipment_types(self) -> List[EquipmentTypeDTO]:
        pass
    
    @abstractmethod
    def update_equipment_type(self, id: int, dto: EquipmentTypeUpdateDTO) -> bool:
        pass
    
    @abstractmethod
    def delete_equipment_type(self, id: int) -> bool:
        pass
