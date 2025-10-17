from mainContext.application.ports.equipment_repo import EquipmentRepo
from mainContext.domain.models.Equipment import Equipment
from typing import Optional


class DeleteEquipment:
    def __init__(self, repo : EquipmentRepo):
        self.repo = repo

    def execute(self, equipment_id: int) -> bool:
        existing_equipment: Optional[Equipment] = self.repo.get_equipment_by_id(equipment_id)
        if not existing_equipment:
            return False
        return self.repo.delete_equipment(equipment_id)