from mainContext.application.ports.Foir02RequiredEquipmentRepo import Foir02RequiredEquipmentRepo
from mainContext.application.dtos.foir02_required_equipment_dto import Foir02RequiredEquipmentDTO, Foir02RequiredEquipmentCreateDTO, Foir02RequiredEquipmentUpdateDTO
from typing import List, Optional

class CreateFoir02RequiredEquipment:
    def __init__(self, repo: Foir02RequiredEquipmentRepo):
        self.repo = repo
    
    def execute(self, dto: Foir02RequiredEquipmentCreateDTO) -> int:
        return self.repo.create_foir02_required_equipment(dto)

class GetFoir02RequiredEquipmentById:
    def __init__(self, repo: Foir02RequiredEquipmentRepo):
        self.repo = repo
    
    def execute(self, id: int) -> Optional[Foir02RequiredEquipmentDTO]:
        return self.repo.get_foir02_required_equipment_by_id(id)

class GetAllFoir02RequiredEquipment:
    def __init__(self, repo: Foir02RequiredEquipmentRepo):
        self.repo = repo
    
    def execute(self) -> List[Foir02RequiredEquipmentDTO]:
        return self.repo.get_all_foir02_required_equipment()

class UpdateFoir02RequiredEquipment:
    def __init__(self, repo: Foir02RequiredEquipmentRepo):
        self.repo = repo
    
    def execute(self, id: int, dto: Foir02RequiredEquipmentUpdateDTO) -> bool:
        return self.repo.update_foir02_required_equipment(id, dto)

class DeleteFoir02RequiredEquipment:
    def __init__(self, repo: Foir02RequiredEquipmentRepo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_foir02_required_equipment(id)
