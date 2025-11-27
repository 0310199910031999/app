from mainContext.application.ports.equipment_repo import EquipmentRepo
from mainContext.application.dtos.Equipment.equipment_by_property_dto import EquipmentByPropertyDTO
from typing import List

class GetEquipmentByProperty:
    def __init__(self, repo: EquipmentRepo):
        self.repo = repo

    def execute(self, property: str) -> List[EquipmentByPropertyDTO]:
        return self.repo.get_equipment_by_property(property)
