from mainContext.application.ports.equipment_repo import EquipmentRepo
from mainContext.domain.models.Equipment import Equipment
from mainContext.application.dtos.Equipment.create_equipment_dto import CreateEquipmentDTO
from mainContext.application.mappers.Equipment.equipment_mapper import dto_to_equipment

class CreateEquipment:
    def __init__(self, repo : EquipmentRepo):
        self.repo = repo

    def execute(self, dto: CreateEquipmentDTO) -> Equipment:
        equipment = dto_to_equipment(dto)
        return self.repo.create_equipment(equipment)