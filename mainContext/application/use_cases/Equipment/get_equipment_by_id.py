from mainContext.application.ports.equipment_repo import EquipmentRepo
from mainContext.domain.models.Equipment import Equipment
from typing import Optional

class GetEquipmentById:
    def __init__(self, repo : EquipmentRepo):
        self.repo = repo

    def execute(self, equipment_id: int) -> Optional[Equipment]:
        return self.repo.get_equipment_by_id(equipment_id)