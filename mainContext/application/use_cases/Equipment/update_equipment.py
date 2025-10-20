# application/use_cases/equipment/update_equipment.py
from mainContext.application.ports.equipment_repo import EquipmentRepo
from mainContext.application.dtos.Equipment.update_equipment_dto import UpdateEquipmentDTO
from mainContext.application.mappers.Equipment.equipment_mapper import dto_to_updated_equipment

class UpdateEquipmentUseCase:
    def __init__(self, repo: EquipmentRepo):
        self.repo = repo

    def execute(self, equipment_id: int, dto: UpdateEquipmentDTO):
        existing = self.repo.get_equipment_by_id(equipment_id)
        if not existing:
            return None
        updated = dto_to_updated_equipment(dto, existing)
        return self.repo.update_equipment(equipment_id, updated)