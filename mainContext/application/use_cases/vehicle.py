from typing import List, Optional

from mainContext.application.dtos.vehicle_dto import (
    VehicleCreateDTO,
    VehicleDTO,
    VehicleTableRowDTO,
    VehicleUpdateDTO,
)
from mainContext.application.ports.vehicle_repo import VehicleRepo
from mainContext.domain.models.Vehicle import Vehicle


class CreateVehicle:
    def __init__(self, repo: VehicleRepo):
        self.repo = repo

    def execute(self, dto: VehicleCreateDTO) -> int:
        return self.repo.create_vehicle(dto)


class GetVehicleById:
    def __init__(self, repo: VehicleRepo):
        self.repo = repo

    def execute(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.repo.get_vehicle_by_id(vehicle_id)


class ListVehicles:
    def __init__(self, repo: VehicleRepo):
        self.repo = repo

    def execute(self) -> List[Vehicle]:
        return self.repo.list_vehicles()


class ListVehiclesTable:
    def __init__(self, repo: VehicleRepo):
        self.repo = repo

    def execute(self) -> List[VehicleTableRowDTO]:
        return self.repo.list_vehicles_table()


class UpdateVehicle:
    def __init__(self, repo: VehicleRepo):
        self.repo = repo

    def execute(self, vehicle_id: int, dto: VehicleUpdateDTO) -> bool:
        return self.repo.update_vehicle(vehicle_id, dto)


class DeleteVehicle:
    def __init__(self, repo: VehicleRepo):
        self.repo = repo

    def execute(self, vehicle_id: int) -> bool:
        return self.repo.delete_vehicle(vehicle_id)
