from abc import ABC, abstractmethod
from typing import List, Optional

from mainContext.application.dtos.vehicle_dto import (
    VehicleCreateDTO,
    VehicleDTO,
    VehicleTableRowDTO,
    VehicleUpdateDTO,
)
from mainContext.domain.models.Vehicle import Vehicle


class VehicleRepo(ABC):
    @abstractmethod
    def create_vehicle(self, dto: VehicleCreateDTO) -> int:
        pass

    @abstractmethod
    def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        pass

    @abstractmethod
    def list_vehicles(self) -> List[Vehicle]:
        pass

    @abstractmethod
    def list_vehicles_table(self) -> List[VehicleTableRowDTO]:
        pass

    @abstractmethod
    def update_vehicle(self, vehicle_id: int, dto: VehicleUpdateDTO) -> bool:
        pass

    @abstractmethod
    def delete_vehicle(self, vehicle_id: int) -> bool:
        pass
