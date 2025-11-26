from mainContext.application.ports.EquipmentBrandRepo import EquipmentBrandRepo
from mainContext.application.dtos.equipment_brand_dto import EquipmentBrandDTO, EquipmentBrandCreateDTO, EquipmentBrandUpdateDTO
from typing import List, Optional

class CreateEquipmentBrand:
    def __init__(self, repo: EquipmentBrandRepo):
        self.repo = repo
    
    def execute(self, dto: EquipmentBrandCreateDTO) -> int:
        return self.repo.create_equipment_brand(dto)

class GetEquipmentBrandById:
    def __init__(self, repo: EquipmentBrandRepo):
        self.repo = repo
    
    def execute(self, id: int) -> Optional[EquipmentBrandDTO]:
        return self.repo.get_equipment_brand_by_id(id)

class GetAllEquipmentBrands:
    def __init__(self, repo: EquipmentBrandRepo):
        self.repo = repo
    
    def execute(self) -> List[EquipmentBrandDTO]:
        return self.repo.get_all_equipment_brands()

class UpdateEquipmentBrand:
    def __init__(self, repo: EquipmentBrandRepo):
        self.repo = repo
    
    def execute(self, id: int, dto: EquipmentBrandUpdateDTO) -> bool:
        return self.repo.update_equipment_brand(id, dto)

class DeleteEquipmentBrand:
    def __init__(self, repo: EquipmentBrandRepo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_equipment_brand(id)
