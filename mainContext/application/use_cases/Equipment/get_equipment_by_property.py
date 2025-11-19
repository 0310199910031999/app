from mainContext.application.ports.equipment_repo import EquipmentRepo
from mainContext.domain.models.Equipment import Equipment
from typing import List

class GetEquipmentByProperty:
    def __init__(self, repo: EquipmentRepo):
        self.repo = repo

    def execute(self, property: str) -> List[Equipment]:
        return self.repo.get_equipment_by_property(property)
