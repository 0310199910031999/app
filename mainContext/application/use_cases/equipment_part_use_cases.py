from typing import List, Optional

from mainContext.application.ports.EquipmentPartRepo import EquipmentPartRepo
from mainContext.application.dtos.equipment_part_dto import (
    EquipmentPartDTO,
    EquipmentPartCreateDTO,
    EquipmentPartUpdateDTO,
)


class CreateEquipmentPart:
    def __init__(self, repo: EquipmentPartRepo):
        self.repo = repo

    def execute(self, dto: EquipmentPartCreateDTO) -> int:
        return self.repo.create_equipment_part(dto)


class GetEquipmentPartById:
    def __init__(self, repo: EquipmentPartRepo):
        self.repo = repo

    def execute(self, part_id: int) -> Optional[EquipmentPartDTO]:
        return self.repo.get_equipment_part_by_id(part_id)


class GetEquipmentPartsByEquipment:
    def __init__(self, repo: EquipmentPartRepo):
        self.repo = repo

    def execute(self, equipment_id: int) -> List[EquipmentPartDTO]:
        return self.repo.get_equipment_parts_by_equipment(equipment_id)


class GetAllEquipmentParts:
    def __init__(self, repo: EquipmentPartRepo):
        self.repo = repo

    def execute(self) -> List[EquipmentPartDTO]:
        return self.repo.get_all_equipment_parts()


class UpdateEquipmentPart:
    def __init__(self, repo: EquipmentPartRepo):
        self.repo = repo

    def execute(self, part_id: int, dto: EquipmentPartUpdateDTO) -> bool:
        return self.repo.update_equipment_part(part_id, dto)


class DeleteEquipmentPart:
    def __init__(self, repo: EquipmentPartRepo):
        self.repo = repo

    def execute(self, part_id: int) -> bool:
        return self.repo.delete_equipment_part(part_id)
