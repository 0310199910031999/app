from mainContext.application.ports.equipment_repo import EquipmentRepo


class UpdateEquipmentHourometer:
    def __init__(self, repo: EquipmentRepo):
        self.repo = repo

    def execute(self, equipment_id: int, hourometer: float) -> bool:
        return self.repo.update_equipment_hourometer(equipment_id, hourometer)
