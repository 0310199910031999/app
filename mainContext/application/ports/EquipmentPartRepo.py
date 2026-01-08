from abc import ABC, abstractmethod
from typing import List, Optional

from mainContext.application.dtos.equipment_part_dto import (
    EquipmentPartDTO,
    EquipmentPartCreateDTO,
    EquipmentPartUpdateDTO,
)


class EquipmentPartRepo(ABC):
    @abstractmethod
    def create_equipment_part(self, dto: EquipmentPartCreateDTO) -> int:
        pass

    @abstractmethod
    def get_equipment_part_by_id(self, part_id: int) -> Optional[EquipmentPartDTO]:
        pass

    @abstractmethod
    def get_equipment_parts_by_equipment(self, equipment_id: int) -> List[EquipmentPartDTO]:
        pass

    @abstractmethod
    def get_all_equipment_parts(self) -> List[EquipmentPartDTO]:
        pass

    @abstractmethod
    def update_equipment_part(self, part_id: int, dto: EquipmentPartUpdateDTO) -> bool:
        pass

    @abstractmethod
    def delete_equipment_part(self, part_id: int) -> bool:
        pass
