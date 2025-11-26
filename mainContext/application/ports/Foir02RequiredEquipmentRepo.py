from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.foir02_required_equipment_dto import Foir02RequiredEquipmentDTO, Foir02RequiredEquipmentCreateDTO, Foir02RequiredEquipmentUpdateDTO

class Foir02RequiredEquipmentRepo(ABC):
    @abstractmethod
    def create_foir02_required_equipment(self, dto: Foir02RequiredEquipmentCreateDTO) -> int:
        pass
    
    @abstractmethod
    def get_foir02_required_equipment_by_id(self, id: int) -> Optional[Foir02RequiredEquipmentDTO]:
        pass
    
    @abstractmethod
    def get_all_foir02_required_equipment(self) -> List[Foir02RequiredEquipmentDTO]:
        pass
    
    @abstractmethod
    def update_foir02_required_equipment(self, id: int, dto: Foir02RequiredEquipmentUpdateDTO) -> bool:
        pass
    
    @abstractmethod
    def delete_foir02_required_equipment(self, id: int) -> bool:
        pass
