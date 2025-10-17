from mainContext.application.ports.equipment_repo import EquipmentRepo
from mainContext.domain.models.Equipment import Equipment
from typing import List

class ListEquipmentByClient:
    def __init__(self, repo : EquipmentRepo):
        self.repo = repo

    def execute(self, client_id: str) -> List[Equipment]:
        return self.repo.list_by_client_id(client_id)