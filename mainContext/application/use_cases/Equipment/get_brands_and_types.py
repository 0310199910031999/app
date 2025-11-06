from mainContext.application.ports.equipment_repo import EquipmentRepo
from mainContext.application.dtos.Equipment.brands_types_dto import BrandsTypesDTO
from typing import Optional

class GetBrandsAndTypes: 
    def __init__(self, equipment_repo: EquipmentRepo):
        self.equipment_repo = equipment_repo

    def execute(self) -> BrandsTypesDTO:
        return self.equipment_repo.get_brands_and_types()