from mainContext.application.ports.equipment_repo import EquipmentRepo

class EndEquipmentRental:
    def __init__(self, repo: EquipmentRepo):
        self.repo = repo

    def execute(self, equipment_id: int) -> bool:
        return self.repo.end_equipment_rental(equipment_id)
