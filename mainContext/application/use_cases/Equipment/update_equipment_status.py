from mainContext.application.ports.equipment_repo import EquipmentRepo

class UpdateEquipmentStatus:
    def __init__(self, repo: EquipmentRepo):
        self.repo = repo

    def execute(self, equipment_id: int, status: str) -> bool:
        return self.repo.update_equipment_status(equipment_id, status)
