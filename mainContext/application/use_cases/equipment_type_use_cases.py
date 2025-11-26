from mainContext.application.ports.EquipmentTypeRepo import EquipmentTypeRepo
from mainContext.application.dtos.equipment_type_dto import EquipmentTypeDTO, EquipmentTypeCreateDTO, EquipmentTypeUpdateDTO
from typing import List, Optional

class CreateEquipmentType:
    def __init__(self, repo: EquipmentTypeRepo):
        self.repo = repo
    
    def execute(self, dto: EquipmentTypeCreateDTO) -> int:
        return self.repo.create_equipment_type(dto)

class GetEquipmentTypeById:
    def __init__(self, repo: EquipmentTypeRepo):
        self.repo = repo
    
    def execute(self, id: int) -> Optional[EquipmentTypeDTO]:
        return self.repo.get_equipment_type_by_id(id)

class GetAllEquipmentTypes:
    def __init__(self, repo: EquipmentTypeRepo):
        self.repo = repo
    
    def execute(self) -> List[EquipmentTypeDTO]:
        return self.repo.get_all_equipment_types()

class UpdateEquipmentType:
    def __init__(self, repo: EquipmentTypeRepo):
        self.repo = repo
    
    def execute(self, id: int, dto: EquipmentTypeUpdateDTO) -> bool:
        return self.repo.update_equipment_type(id, dto)

class DeleteEquipmentType:
    def __init__(self, repo: EquipmentTypeRepo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_equipment_type(id)
